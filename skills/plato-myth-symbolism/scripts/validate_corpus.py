#!/usr/bin/env python3
"""Validate the curated Plato myth and symbolism learning corpus without dependencies."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


CLAIM_LAYERS = {"textual-observation", "contextual-inference", "interpretive-boundary", "reception"}


def load_records(data_dir: Path, filename: str) -> list[dict[str, Any]]:
    path = data_dir / filename
    with path.open(encoding="utf-8") as handle:
        records = json.load(handle)
    if not isinstance(records, list):
        raise ValueError(f"{filename} must contain a JSON array")
    return records


def required(record: dict[str, Any], keys: set[str], label: str, errors: list[str]) -> None:
    missing = sorted(
        key
        for key in keys
        if key not in record
        or record[key] is None
        or (isinstance(record[key], str) and not record[key].strip())
    )
    if missing:
        errors.append(f"{label} {record.get('id', '<missing id>')}: missing {', '.join(missing)}")


def unique_ids(records: list[dict[str, Any]], label: str, errors: list[str]) -> set[str]:
    seen: set[str] = set()
    for record in records:
        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id:
            errors.append(f"{label}: record has no string id")
        elif record_id in seen:
            errors.append(f"{label}: duplicate id {record_id}")
        else:
            seen.add(record_id)
    return seen


def validate_dataset(data_dir: Path) -> list[str]:
    errors: list[str] = []
    sources = load_records(data_dir, "sources.json")
    cards = load_records(data_dir, "myth_cards.json")
    claims = load_records(data_dir, "claims.json")
    concepts = load_records(data_dir, "concepts.json")
    maps = load_records(data_dir, "argument_maps.json")

    source_ids = unique_ids(sources, "sources", errors)
    card_ids = unique_ids(cards, "myth cards", errors)
    unique_ids(claims, "claims", errors)
    unique_ids(concepts, "concepts", errors)
    unique_ids(maps, "argument maps", errors)

    for source in sources:
        required(source, {"id", "title", "work", "kind", "uri", "license_notice", "reuse_policy", "accessed"}, "source", errors)
        if not source.get("uri", "").startswith("https://"):
            errors.append(f"source {source.get('id')}: uri must use https")

    required_card_keys = {"id", "title", "dialogue", "stephanus", "speaker", "audience", "narrative_status", "argument_context", "primary_source_id", "analysis_prompts", "non_claims"}
    for card in cards:
        required(card, required_card_keys, "myth card", errors)
        if "book" not in card:
            errors.append(f"myth card {card.get('id')}: missing book field")
        stephanus = card.get("stephanus", {})
        if not isinstance(stephanus, dict) or not stephanus.get("start") or not stephanus.get("end"):
            errors.append(f"myth card {card.get('id')}: requires Stephanus start and end")
        if card.get("primary_source_id") not in source_ids:
            errors.append(f"myth card {card.get('id')}: unknown primary source")
        if len(card.get("analysis_prompts", [])) < 2:
            errors.append(f"myth card {card.get('id')}: needs two analysis prompts")
        if not card.get("non_claims"):
            errors.append(f"myth card {card.get('id')}: needs an explicit non-claim")

    for claim in claims:
        required(claim, {"id", "statement", "claim_layer", "supporting_card_ids", "limit_note"}, "claim", errors)
        if claim.get("claim_layer") not in CLAIM_LAYERS:
            errors.append(f"claim {claim.get('id')}: invalid claim layer")
        for card_id in claim.get("supporting_card_ids", []):
            if card_id not in card_ids:
                errors.append(f"claim {claim.get('id')}: unknown card {card_id}")

    for concept in concepts:
        required(concept, {"id", "greek", "transliteration", "translation_options", "use_note", "card_ids"}, "concept", errors)
        if not concept.get("translation_options"):
            errors.append(f"concept {concept.get('id')}: needs translation options")
        for card_id in concept.get("card_ids", []):
            if card_id not in card_ids:
                errors.append(f"concept {concept.get('id')}: unknown card {card_id}")

    for argument_map in maps:
        required(argument_map, {"id", "card_id", "problem", "image_or_narrative", "analytic_function", "unresolved_point"}, "argument map", errors)
        if argument_map.get("card_id") not in card_ids:
            errors.append(f"argument map {argument_map.get('id')}: unknown card")

    by_id = {card["id"]: card for card in cards if isinstance(card.get("id"), str)}
    cave = by_id.get("republic-cave")
    if not cave or cave.get("dialogue") != "Republic" or cave.get("stephanus") != {"start": "514a", "end": "521b"} or cave.get("speaker") != "Socrates" or cave.get("audience") != "Glaucon":
        errors.append("boundary: Cave must remain Republic VII 514a–521b, Socrates to Glaucon")
    aristophanes = by_id.get("symposium-aristophanes")
    if not aristophanes or aristophanes.get("speaker") != "Aristophanes" or aristophanes.get("dialogue") != "Symposium":
        errors.append("boundary: divided humans must remain Aristophanes' Symposium speech")
    atlantis = by_id.get("timaeus-atlantis")
    if not atlantis or atlantis.get("dialogue") != "Timaeus" or atlantis.get("speaker") != "Critias" or "not archaeological proof" not in atlantis.get("non_claims", []):
        errors.append("boundary: Atlantis must remain a Critias Timaeus frame with no archaeological-proof claim")
    er = by_id.get("republic-er")
    if not er or "not empirical afterlife evidence" not in er.get("non_claims", []):
        errors.append("boundary: Myth of Er must retain its empirical-proof limit")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path(__file__).resolve().parents[1] / "data")
    args = parser.parse_args()
    errors = validate_dataset(args.data_dir)
    if errors:
        print("Corpus validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Corpus validation passed: curated Plato cards, claims, and boundaries are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

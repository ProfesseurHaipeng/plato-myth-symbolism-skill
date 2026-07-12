---
name: plato-myth-symbolism
license: MIT
description: Interpret Platonic myths through primary texts, philosophical function, historical context, and competing scholarly readings. Use when Codex is asked about Plato's cave, Myth of Er, Symposium's divided humans, Atlantis, souls, justice, or Greek philosophical storytelling.
---

# Plato Myth and Symbolism

Read a Platonic myth as an argument-bearing literary form, not as a factual report of a supernatural event. Keep Plato's dramatic speaker, dialogue setting, surrounding argument, and later reception distinct.

## Runtime: Python 3.10+

The bundled validator uses the standard library only.

This is a learning and analysis skill. It should show an AI how to locate a passage, separate textual fact from interpretation, map the argument a narrative serves, compare readings, and state what the text cannot establish.

## Workflow

1. Locate the primary passage and cite dialogue, Stephanus range, speaker, audience, Greek term when useful, and translation used. Start with [classical-corpus.md](references/classical-corpus.md) and [sources.md](references/sources.md).
2. Load the matching card from `data/myth_cards.json`; do not create a story from memory when a source-grounded card exists.
3. Summarize the immediate argument before interpreting the myth. Ask what problem the myth addresses: knowledge, education, justice, eros, soul, politics, cosmology, or the limits of proof.
4. Track speaker and audience. A myth told by Socrates is not automatically Plato's literal doctrine; compare the narrator's confidence and the dialogue's irony.
5. Separate textual observation, philological inference, philosophical interpretation, later allegory, and modern creative adaptation.
6. Compare at least two plausible readings. State what each explains and what it leaves unresolved.
7. End with a reflective question or research path, not a deterministic moral or metaphysical verdict.
8. Use this answer order: **textual record → dramatic and argumentative context → concepts → competing readings → limits → next learning step**.

## Research assets

Use [learning-path.md](references/learning-path.md), [dialogue-matrix.md](references/dialogue-matrix.md), and [interpretation-sheet.md](references/interpretation-sheet.md). Run `python3 scripts/validate_corpus.py` after editing the source-grounded cards.

The starter corpus is a scaffold for study, not a replacement for a full primary text. Use its source ids and Stephanus locators; do not invent quotations or silently replace a dramatic speaker with “Plato.”

## Scope examples

- Cave: distinguish the image, education/turning language, political return, and later “simulation” adaptations.
- Myth of Er: distinguish eschatological narrative, choice, responsibility, and the dialogue's closing exhortation.
- Symposium: distinguish Aristophanes' comic speech from Diotima's account and from the dialogue's broader account of eros.
- Atlantis: distinguish the Timaeus/Critias narrative context from modern lost-continent claims.

## Non-negotiable boundaries

- Aristophanes' divided humans are Aristophanes' speech in the *Symposium*, not Diotima's teaching and not Plato's unqualified final doctrine.
- The Cave is a *Republic* image tied to education and political return; it is not evidence of a literal prison, simulation, or neurological model.
- The Myth of Er and the judgment myths are philosophical narratives, not empirical proof of an afterlife.
- Atlantis belongs to the *Timaeus* / unfinished *Critias* frame and cannot establish an archaeological location.

Do not present Plato's myths as historical proof, archaeological evidence, psychology, or a substitute for professional advice. Do not fabricate a Greek quotation; link to the text or state that you are paraphrasing.

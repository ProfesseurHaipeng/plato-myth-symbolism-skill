# Plato Myth and Symbolism Skill

Standalone Skill for learning and researching Platonic myths, images, and philosophical storytelling through primary-text location, dramatic voice, argument structure, Greek concepts, competing readings, and reception history.

It gives an AI a repeatable method:

1. locate a dialogue and Stephanus range;
2. identify speaker, audience, and narrative frame;
3. reconstruct the nearby philosophical problem;
4. distinguish textual observation from interpretation and later reception;
5. compare defensible readings and name their limits;
6. give a next learning question rather than a deterministic verdict.

## What is included

- a curated starter corpus of 13 myth/image cards spanning *Republic*, *Symposium*, *Phaedrus*, *Phaedo*, *Gorgias*, *Statesman*, and *Timaeus*;
- source, claim, myth-card, concept, and argument-map data under `skills/plato-myth-symbolism/data/`;
- source/claim JSON Schemas and a no-dependency validator;
- learning workflows and tests for high-risk errors: speaker confusion, false afterlife proof, and Atlantis-as-archaeology.

## Local verification

```bash
cd skills/plato-myth-symbolism
python3 scripts/validate_corpus.py
python3 -m unittest discover -s tests -v
```

Install with `gh skill install ProfesseurHaipeng/plato-myth-symbolism-skill --skill plato-myth-symbolism --pin v0.2.0`.

The Skill is source-grounded humanities research. It does not treat myths as history, archaeology, empirical cosmology, clinical psychology, or a substitute for professional advice.

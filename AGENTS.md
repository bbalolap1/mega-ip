# AGENTS.md

## Project Identity

This repository builds the **Mega IP Narrative Sandbox**.

The software exists to visualize, organize, explore, and revise the user's Mega IP Universe.

It is not primarily:
- a conventional game
- a novel-writing application
- a comic generator
- a movie-production system
- a Minecraft clone

It is a programmable narrative world: a visual and interactive sandbox where lore stored in Markdown becomes structured data, scenes, timelines, characters, philosophies, branches, and world views.

## Highest Priority

Preserve the creator's intended lore.

Do not silently:
- invent canon
- rewrite the cosmology
- merge unresolved ideas into fixed canon
- replace the user's terminology
- redesign the project into a conventional game
- add unrelated mechanics
- overbuild the first version

## Source of Truth

The `/lore` directory is the authoritative creative source.

The file `/FOUNDATION.md` contains the initial software and universe foundation.

Structured JSON or database records are derived representations only. They must never replace the original Markdown source.

## Canon Statuses

Every lore entity must use one of these statuses:

- `canon`
- `provisional`
- `unresolved`
- `alternative`
- `experiment`
- `archived`
- `removed`

Rules:
1. `canon` content is official.
2. `provisional` content is usable but unsettled.
3. `unresolved` content must not be completed by invention.
4. `alternative` content belongs to a separate branch.
5. `experiment` content is temporary.
6. `archived` content remains accessible but inactive.
7. `removed` content must not appear in active views.

## Version 0.0 Objective

Build a small, understandable, runnable Streamlit prototype that proves this loop:

```text
Write lore
↓
Load lore
↓
Visualize lore
↓
Edit lore
↓
Create an alternative branch
↓
See the changed narrative without altering canon
```

## Version 0.0 Required Pages

1. **Universe**
   - Shows Prime Reality, the Omniverse, Nana, the Abyss, divine realms, and important worlds.
   - Uses simple cards or expandable sections.
   - Does not require 3D.

2. **Chronicle**
   - Shows Ordos' current narrative progression as an ordered timeline.
   - Each event may open into details.

3. **Characters**
   - Starts with Ordos.
   - Shows identity, origin, classification, domain, beliefs, philosophy, canon status, and linked events.

4. **Lore Editor**
   - Opens Markdown files from `/lore`.
   - Allows editing and saving.
   - Requires an explicit save action.
   - Never silently changes lore.

5. **Scene Viewer**
   - Displays the first scene: **Ordos' First Divine Decision**.
   - Uses text, scene beats, simple visual panels, and optional placeholder images.
   - Does not require animation or 3D.

6. **Branch Creator**
   - Creates an alternative branch from a selected canon event.
   - Stores branches separately from canon.
   - Never overwrites the canon file.

## Required Technical Stack

Use:
- Python 3.11+
- Streamlit
- Markdown files
- YAML frontmatter
- JSON for generated cache data
- SQLite only if genuinely needed

Prefer standard-library solutions where practical.

## Code Quality Rules

1. Keep modules small and clearly named.
2. Explain non-obvious code with comments.
3. Use type hints.
4. Add basic exception handling.
5. Validate Markdown frontmatter.
6. Never modify unrelated files.
7. Do not introduce frameworks not required for Version 0.0.
8. Keep the code understandable to a beginner.
9. Include a README with exact run commands.
10. Include a requirements.txt.
11. Include at least basic parser and branch-safety tests.

## Required Repository Structure

```text
mega-ip-narrative-sandbox/
├── AGENTS.md
├── FOUNDATION.md
├── README.md
├── requirements.txt
├── app.py
│
├── lore/
│   ├── cosmology/
│   ├── characters/
│   ├── worlds/
│   ├── gods/
│   ├── domains/
│   ├── civilizations/
│   ├── philosophies/
│   ├── events/
│   ├── timelines/
│   └── scenes/
│
├── app/
│   ├── models.py
│   ├── lore_parser.py
│   ├── canon_controller.py
│   ├── universe_navigator.py
│   ├── timeline_engine.py
│   ├── character_engine.py
│   ├── scene_engine.py
│   ├── branch_engine.py
│   └── file_utils.py
│
├── data/
│   └── generated/
│
├── assets/
│   ├── characters/
│   ├── worlds/
│   ├── maps/
│   ├── audio/
│   └── scenes/
│
├── branches/
│   ├── alternatives/
│   └── experiments/
│
└── tests/
    ├── test_lore_parser.py
    └── test_branch_engine.py
```

## Initial Lore Files

Create initial Markdown files based only on `FOUNDATION.md`:

- `lore/characters/ordos.md`
- `lore/worlds/nana.md`
- `lore/cosmology/omniverse.md`
- `lore/cosmology/abyss.md`
- `lore/philosophies/ordos-divinity.md`
- `lore/events/ordos-first-divine-decision.md`
- `lore/timelines/ordos-main-timeline.md`
- `lore/scenes/ordos-first-divine-decision.md`

Mark unsettled details as `unresolved` or `provisional`.

## First Scene

The first scene must preserve this sequence:

1. Ordos exists within Nana.
2. He recognizes his divine shadow.
3. The shadow communicates its philosophy.
4. Ordos compares it with his memories of Earth.
5. He rejects the idea that good and evil must be balanced.
6. He removes the shadow.
7. His divine nature changes.
8. Nana reacts.
9. Other Origin Gods observe the change.
10. The first philosophical conflict begins.

Do not invent final dialogue unless clearly marked as placeholder or provisional.

## Completion Definition

Version 0.0 is complete when:

- `streamlit run app.py` launches successfully.
- All six required pages are accessible.
- Markdown lore loads correctly.
- Ordos and the initial cosmology appear in the interface.
- The first scene is readable in the Scene Viewer.
- A user can edit a lore file and save it.
- A user can create an alternative branch without altering canon.
- Tests pass.
- README instructions are complete.

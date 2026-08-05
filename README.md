# Mega IP Narrative Sandbox

Version 0.0 is a small Streamlit prototype for visualizing and safely editing the Mega IP Universe.

The app is not a conventional game. It is a programmable narrative sandbox where Markdown lore remains the source of truth and the interface turns that lore into readable universe, chronicle, character, scene, editor, and branch views.

## Features in Version 0.0

- **Universe** page with Prime Reality, the Omniverse, Nana, the Abyss, divine realms, and important worlds.
- **Chronicle** page for Ordos' ordered progression.
- **Characters** page beginning with Ordos.
- **Lore Editor** with explicit validation and save action. It does not autosave.
- **Scene Viewer** for **Ordos' First Divine Decision**.
- **Branch Creator** that writes alternatives and experiments under `branches/` without overwriting canon lore.

## Install

Use Python 3.11 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## Test

```bash
python -m pytest
```

## Lore source of truth

Lore lives in `lore/` as Markdown files with YAML frontmatter. Generated JSON or future databases are only derived forms and must not replace the Markdown source.

Every lore entity must use one canon status:

- `canon`
- `provisional`
- `unresolved`
- `alternative`
- `experiment`
- `archived`
- `removed`

## Initial lore files

Version 0.0 includes initial files for Ordos, Nana, the Omniverse, the Abyss, Ordos' divinity, the first divine decision event, Ordos' main timeline, and the first scene.

Unsettled material is marked `provisional` or `unresolved` rather than being silently completed.

## Version 0.1 ideas

- Add generated JSON cache files in `data/generated/`.
- Add richer philosophy comparison views.
- Add branch comparison views that show canon beside alternatives.
- Add relationship links between characters, worlds, events, and philosophies.
- Add optional placeholder images without changing lore canon.

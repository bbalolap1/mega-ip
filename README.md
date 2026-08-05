# Mega IP Narrative Sandbox

Version 0.0 is a small Streamlit prototype for visualizing and safely editing the Mega IP Universe.

The app is not a conventional game. It is a programmable narrative sandbox where Markdown lore remains the source of truth and the interface turns that lore into readable universe, chronicle, character, scene, editor, and branch views.

## Features in Version 0.0

- **Universe** page with a visual relationship map for Prime Reality, the Omniverse, Nana, the Abyss, divine realms, and important worlds.
- **Chronicle** page for Ordos' ordered progression, grouped into readable narrative arcs instead of a flat developer list.
- **Characters** page beginning with Ordos while clearly explaining that Ordos is the first loaded character, not the limit of the sandbox.
- **Lore Editor** with explicit validation and save action. It does not autosave.
- **Scene Viewer** for **Ordos' First Divine Decision**, presented as a storyboard with cast, panels, narration, provisional dialogue, and consequences.
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

The tests include a lightweight app smoke test that verifies the required Streamlit page wiring with a fake `streamlit` module. This does not replace running the real app, but it catches broken navigation in environments where Streamlit cannot be installed.

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

## UI direction

Streamlit is used only as the Version 0.0 shell. The UI now emphasizes narrative cards, grouped arcs, storyboard panels, and creator-facing status language so the prototype feels closer to a narrative sandbox while still staying small and avoiding 3D.

## Version 0.1 ideas

- Add generated JSON cache files in `data/generated/`.
- Add richer philosophy comparison views.
- Add branch comparison views that show canon beside alternatives.
- Add relationship links between characters, worlds, events, and philosophies.
- Add optional placeholder images without changing lore canon.

## Why the UI is split this way

Version 0.0 uses six sidebar pages because each page protects a different part of the creator workflow:

1. **Universe** answers “what exists and how is it related?”
2. **Chronicle** answers “what happens in Ordos' current progression?”
3. **Characters** answers “who is involved and what do they believe?”
4. **Lore Editor** answers “how do I safely change the Markdown source?”
5. **Scene Viewer** answers “how does one key moment read as a scene?”
6. **Branch Creator** answers “how do I try a different premise without changing canon?”

The Lore Editor has both a template editor and raw Markdown mode. The template handles common fields like `id`, `type`, `status`, `name`, `origin`, `classification`, domain, authority, beliefs, and linked events. Raw Markdown remains available because the Markdown files are still the source of truth.

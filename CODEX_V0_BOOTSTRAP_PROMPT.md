# CODEX VERSION 0.0 BOOTSTRAP PROMPT

Read `AGENTS.md` and `FOUNDATION.md` completely before changing or creating code.

## Mission

Build **Version 0.0** of the Mega IP Narrative Sandbox.

This is a programmable visual narrative universe, not a conventional game.

The application must turn Markdown lore into an understandable interactive software prototype where the creator can:

- explore the universe
- follow the chronicle
- inspect characters
- edit lore
- view a narrative scene
- create alternative branches without changing canon

The Mega IP Universe is the product. The software is the tool used to visualize and develop it.

## Creative Boundaries

Preserve the supplied lore.

Do not:
- invent permanent lore
- redesign Ordos
- redefine Nana
- alter the meaning of Origin Gods or ascended gods
- replace the user's theology, cosmology, cultivation, authority, faith, or eternity concepts
- turn the project into a combat-focused game
- build a generic RPG
- add levels, loot, quests, currencies, or win conditions unless later requested
- introduce 3D in Version 0.0
- silently promote provisional lore into canon

When a detail is missing, use:
- `status: unresolved`, or
- a visibly labeled placeholder

## Required Result

Create a runnable Python and Streamlit application.

The application must have these six pages:

1. Universe
2. Chronicle
3. Characters
4. Lore Editor
5. Scene Viewer
6. Branch Creator

Use a sidebar for navigation.

## Core Data Flow

Implement this exact conceptual flow:

```text
Markdown lore
      ↓
Lore parser
      ↓
Validated structured objects
      ↓
Application views
      ↓
User edits or branch creation
      ↓
Updated lore or separate alternative branch
```

Markdown remains the source of truth.

## Required Features

### Universe Page

Show:
- Prime Reality
- Omniverse
- Nana
- Abyss
- divine realms
- important worlds

Use cards, expanders, and relationship labels.

### Chronicle Page

Show the ordered progression:

- Earth
- human life
- death
- reincarnation
- birth as Ordos
- Origin Godhood
- discovery of divine corruption
- removal of the shadow
- new understanding of godhood
- fellowship with mortals
- angels
- open cultivation
- education and civilization
- ascended gods
- complete divine realms
- conflict between philosophies
- war with the Abyss
- search for true eternity

Clearly label any unsettled final transformation.

### Characters Page

Begin with Ordos.

Show:
- identity
- origin
- classification
- current domain
- authority
- beliefs
- philosophy
- canon status
- linked events
- unresolved questions

### Lore Editor

Allow the user to:
- select a Markdown file
- view its raw content
- edit it
- save explicitly
- see success or validation errors

Do not autosave.

### Scene Viewer

Render the scene **Ordos' First Divine Decision**.

Display:
- scene title
- canon status
- setting
- characters
- narrative beats
- narration
- provisional dialogue
- consequences

Use simple visual styling. Placeholder art panels are acceptable.

### Branch Creator

Allow the user to:
- select a canon event
- name a branch
- choose branch type: alternative or experiment
- add a changed premise
- save the branch separately under `/branches`
- preserve a reference to the source canon event

The branch creator must never overwrite the canon Markdown file.

## Lore Format

Use YAML frontmatter.

Example:

```markdown
---
id: character.ordos
type: character
status: canon
name: Ordos
origin: Earth
classification: Origin God
primary_domain: Order
---

# Central Question

What should a true god become?
```

Create a reusable parser that:
- separates YAML frontmatter from body content
- validates required fields
- returns typed Python objects
- reports readable errors

## Initial Files

Generate the initial lore files listed in `AGENTS.md`.

Base them only on `FOUNDATION.md`.

Do not overfill them.

Keep unresolved material unresolved.

## Technical Requirements

- Python 3.11+
- Streamlit
- PyYAML
- type hints
- basic exception handling
- modular files
- beginner-readable code
- `requirements.txt`
- `README.md`
- tests for the lore parser
- tests proving branch creation does not overwrite canon

## User Experience

Keep the application visually clear.

Use:
- headings
- cards or containers
- expanders
- tabs where useful
- status labels
- clear navigation

Avoid:
- dense developer dashboards
- unnecessary configuration
- overly technical language in the interface

## Required Build Order

1. Create repository structure.
2. Create data models.
3. Create lore parser.
4. Create initial lore files.
5. Create application shell and navigation.
6. Implement each page.
7. Implement branch safety.
8. Add tests.
9. Write README.
10. Run tests and fix failures.
11. Run the application or perform an import-level smoke test.
12. Produce a completion report.

## Completion Report

At the end, report:

- files created
- features completed
- tests run
- unresolved limitations
- exact commands to install and run
- what should be built in Version 0.1

Do not claim a feature works unless it was tested.

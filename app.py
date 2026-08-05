"""Streamlit entry point for Mega IP Narrative Sandbox Version 0.0."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from app.branch_engine import create_branch
from app.canon_controller import is_selectable_canon_event, status_label
from app.character_engine import character_documents, find_ordos
from app.file_utils import list_markdown_files, read_text, write_text
from app.lore_parser import load_lore_documents, split_frontmatter, validate_frontmatter
from app.scene_engine import first_scene, frontmatter_list
from app.timeline_engine import get_main_timeline, timeline_steps
from app.universe_navigator import universe_documents
from app.view_helpers import lore_counts, status_tone, timeline_stage

ROOT = Path(__file__).parent
LORE_ROOT = ROOT / "lore"
BRANCHES_ROOT = ROOT / "branches"


@st.cache_data(show_spinner=False)
def cached_lore() -> list:
    return load_lore_documents(LORE_ROOT)


def refresh_lore() -> None:
    cached_lore.clear()


def apply_visual_theme() -> None:
    """Apply lightweight CSS so Streamlit feels more like a narrative console."""
    st.markdown(
        """
        <style>
        .stApp { background: linear-gradient(180deg, #090b14 0%, #111827 42%, #0f172a 100%); color: #e5e7eb; }
        [data-testid="stSidebar"] { background: #050816; border-right: 1px solid #334155; }
        div[data-testid="stVerticalBlockBorderWrapper"] { border-color: rgba(148, 163, 184, .35); background: rgba(15, 23, 42, .58); }
        .sandbox-hero { padding: 1.2rem 1.4rem; border: 1px solid rgba(125, 211, 252, .35); border-radius: 18px; background: radial-gradient(circle at top left, rgba(56, 189, 248, .22), rgba(15, 23, 42, .72)); margin-bottom: 1rem; }
        .vision-note { padding: .85rem 1rem; border-left: 4px solid #fbbf24; background: rgba(251, 191, 36, .10); border-radius: 10px; margin-bottom: 1rem; }
        .scene-panel { padding: 1rem; border-radius: 16px; border: 1px solid rgba(168, 85, 247, .40); background: linear-gradient(135deg, rgba(88, 28, 135, .26), rgba(15, 23, 42, .88)); min-height: 130px; }
        .status-pill { display: inline-block; padding: .2rem .55rem; border-radius: 999px; background: rgba(34, 197, 94, .16); border: 1px solid rgba(34, 197, 94, .45); font-size: .82rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str) -> None:
    st.markdown(f'<div class="sandbox-hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)


def status_badge(status: str) -> None:
    st.markdown(
        f'<span class="status-pill">{status_label(status)} — {status_tone(status)}</span>',
        unsafe_allow_html=True,
    )


def vision_note() -> None:
    st.markdown(
        '<div class="vision-note"><strong>Vision boundary:</strong> Version 0.0 is a first readable lens for the Mega IP Universe. It is not trying to be the full final interface, a combat game, or a generic RPG.</div>',
        unsafe_allow_html=True,
    )


def page_universe(documents: list) -> None:
    hero("Universe", "A visual-first cosmology map built from Markdown lore, not a 3D simulation yet.")
    vision_note()
    st.markdown("### Reality scale")
    relationship_rows = [
        ("Prime Reality", "context for", "Omniverse"),
        ("Omniverse", "contains", "universes / realms / worlds"),
        ("Nana", "is important world for", "Ordos' first divine decision"),
        ("Abyss", "opposes through", "domination / endless consumption"),
        ("Divine realms", "remain", "important but not fully settled"),
    ]
    for left, relation, right in relationship_rows:
        a, b, c = st.columns([1.2, 0.7, 1.5])
        a.container(border=True).subheader(left)
        b.markdown(f"<br><center>**{relation}**</center>", unsafe_allow_html=True)
        c.container(border=True).write(right)

    st.markdown("### Loaded lore cards")
    for doc in universe_documents(documents):
        with st.expander(f"{doc.name} — {status_label(doc.status)}", expanded=doc.name in {"Nana", "Omniverse", "Abyss"}):
            status_badge(doc.status)
            st.markdown(doc.body)
            st.caption("Structured frontmatter derived from the Markdown source:")
            st.json(doc.frontmatter, expanded=False)


def page_chronicle(documents: list) -> None:
    hero("Chronicle", "Ordos' progression grouped into readable narrative arcs instead of one flat list.")
    timeline = get_main_timeline(documents)
    steps = timeline_steps(timeline)
    if not steps:
        st.error("No valid Ordos main timeline found.")
        return

    grouped: dict[str, list[dict[str, str]]] = {}
    for step in steps:
        grouped.setdefault(timeline_stage(int(step["order"])), []).append(step)

    for stage, stage_steps in grouped.items():
        st.markdown(f"## {stage}")
        cols = st.columns(2)
        for index, step in enumerate(stage_steps):
            with cols[index % 2].container(border=True):
                st.caption(f"Step {step['order']} · {status_label(step['status'])}")
                st.subheader(step["title"])
                st.write(step["summary"])
                if step["status"] == "unresolved":
                    st.warning("Intentionally unresolved: do not finalize by invention.")


def page_characters(documents: list) -> None:
    hero("Characters", "Ordos is the first loaded character, not the intended limit of the sandbox.")
    st.info("Version 0.0 starts with Ordos because the foundation centers him. Future Markdown files can add Origin Gods, ascended gods, mortals, angels, and other entities without changing app code.")
    characters = character_documents(documents)
    ordos = find_ordos(documents)
    if ordos is None:
        st.error("Ordos was not found in lore/characters.")
        return
    selected_name = st.selectbox(
        "Character",
        [doc.name for doc in characters],
        index=[doc.id for doc in characters].index(ordos.id),
    )
    selected = next(doc for doc in characters if doc.name == selected_name)
    st.header(selected.name)
    status_badge(selected.status)
    frontmatter = selected.frontmatter
    tabs = st.tabs(["Identity", "Beliefs", "Links", "Raw lore"])
    with tabs[0]:
        cols = st.columns(3)
        fields = [
            ("Origin", frontmatter.get("origin")),
            ("Classification", frontmatter.get("classification")),
            ("Current domain", frontmatter.get("current_domain") or frontmatter.get("primary_domain")),
            ("Authority", frontmatter.get("authority")),
            ("Philosophy", frontmatter.get("philosophy")),
            ("Canon status", status_label(selected.status)),
        ]
        for index, (label, value) in enumerate(fields):
            with cols[index % 3].container(border=True):
                st.caption(label)
                st.write(value or "Unresolved")
    with tabs[1]:
        for belief in frontmatter.get("beliefs", []):
            st.container(border=True).write(belief)
    with tabs[2]:
        st.subheader("Linked events")
        for event in frontmatter.get("linked_events", []):
            st.write(f"- `{event}`")
        st.subheader("Unresolved questions")
        for question in frontmatter.get("unresolved_questions", []):
            st.warning(question)
    with tabs[3]:
        st.markdown(selected.body)
        st.json(frontmatter, expanded=False)


def page_lore_editor() -> None:
    hero("Lore Editor", "Raw Markdown editing with explicit save; no silent canon changes.")
    files = list_markdown_files(LORE_ROOT)
    choices = {path.relative_to(ROOT).as_posix(): path for path in files}
    selected_label = st.selectbox("Markdown file", list(choices))
    selected_path = choices[selected_label]
    raw_content = read_text(selected_path, LORE_ROOT)
    left, right = st.columns([1.25, 0.75])
    with left:
        edited = st.text_area("Raw Markdown", value=raw_content, height=560)
    with right:
        st.markdown("### Save rules")
        st.write("- Edit only this selected Markdown file.")
        st.write("- Validate frontmatter before writing.")
        st.write("- Save only when the explicit button is pressed.")
        st.write("- Keep canon, provisional, unresolved, alternatives, and experiments distinct.")
    if st.button("Validate and save explicitly", type="primary"):
        try:
            frontmatter, _body = split_frontmatter(edited)
            errors = validate_frontmatter(frontmatter)
            if errors:
                for error in errors:
                    st.error(error)
            else:
                write_text(selected_path, edited, LORE_ROOT)
                refresh_lore()
                st.success(f"Saved {selected_label}.")
        except Exception as exc:  # User-facing editor validation should catch readable failures.
            st.error(f"Could not save: {exc}")


def page_scene_viewer(documents: list) -> None:
    hero("Scene Viewer", "A storyboard-style reading of Ordos' First Divine Decision.")
    scene = first_scene(documents)
    if scene is None:
        st.error("The first scene is missing.")
        return
    st.header(scene.name)
    status_badge(scene.status)
    st.info(f"Setting: {scene.frontmatter.get('setting', 'Unresolved')}")
    st.markdown("### Cast")
    cast_cols = st.columns(len(frontmatter_list(scene, "characters")) or 1)
    for index, character in enumerate(frontmatter_list(scene, "characters")):
        with cast_cols[index].container(border=True):
            st.subheader(character)
            st.caption("Loaded from scene frontmatter")

    st.markdown("### Storyboard beats")
    beats = frontmatter_list(scene, "beats")
    for index, beat in enumerate(beats, start=1):
        st.markdown(f'<div class="scene-panel"><strong>Panel {index}</strong><br>{beat}</div>', unsafe_allow_html=True)

    tabs = st.tabs(["Narration", "Provisional Dialogue", "Consequences", "Source note"])
    with tabs[0]:
        for item in frontmatter_list(scene, "narration"):
            st.container(border=True).write(item)
    with tabs[1]:
        st.warning("Dialogue here is placeholder/provisional, not final canon dialogue.")
        for item in frontmatter_list(scene, "provisional_dialogue"):
            st.container(border=True).write(item)
    with tabs[2]:
        for item in frontmatter_list(scene, "consequences"):
            st.container(border=True).write(item)
    with tabs[3]:
        st.markdown(scene.body)


def page_branch_creator(documents: list) -> None:
    hero("Branch Creator", "Alternative-history creation that preserves canon files.")
    st.write("Select a canon event, name a branch, and record the changed premise separately under `/branches`.")
    events = [doc for doc in documents if is_selectable_canon_event(doc)]
    if not events:
        st.error("No canon events are available for branching.")
        return
    event_labels = {f"{doc.name} ({doc.id})": doc for doc in events}
    selected_label = st.selectbox("Source canon event", list(event_labels))
    selected_event = event_labels[selected_label]
    with st.expander("Source canon event preview", expanded=True):
        status_badge(selected_event.status)
        st.markdown(selected_event.body)
    branch_name = st.text_input("Branch name")
    branch_type = st.radio("Branch type", ["alternative", "experiment"], horizontal=True)
    changed_premise = st.text_area("Changed premise", height=180)
    if st.button("Save branch separately", type="primary"):
        try:
            record = create_branch(selected_event, branch_name, branch_type, changed_premise, BRANCHES_ROOT)
            st.success(f"Created branch {record.branch_id} at {record.path.relative_to(ROOT)}.")
            st.info("The source canon event file was not overwritten.")
        except Exception as exc:
            st.error(f"Could not create branch: {exc}")


def main() -> None:
    st.set_page_config(page_title="Mega IP Narrative Sandbox", layout="wide")
    apply_visual_theme()
    st.sidebar.title("Mega IP Narrative Sandbox")
    st.sidebar.caption("Version 0.0 · narrative lens")
    page = st.sidebar.radio(
        "Navigate",
        ["Universe", "Chronicle", "Characters", "Lore Editor", "Scene Viewer", "Branch Creator"],
    )
    documents = cached_lore()
    invalid = [doc for doc in documents if not doc.is_valid]
    if invalid:
        st.sidebar.error(f"{len(invalid)} lore file(s) have validation errors.")
    counts = lore_counts(documents)
    st.sidebar.markdown("### Loaded lore")
    for lore_type, count in sorted(counts.items()):
        st.sidebar.caption(f"{lore_type}: {count}")
    st.sidebar.caption("Markdown lore remains the source of truth.")

    if page == "Universe":
        page_universe(documents)
    elif page == "Chronicle":
        page_chronicle(documents)
    elif page == "Characters":
        page_characters(documents)
    elif page == "Lore Editor":
        page_lore_editor()
    elif page == "Scene Viewer":
        page_scene_viewer(documents)
    else:
        page_branch_creator(documents)


if __name__ == "__main__":
    main()

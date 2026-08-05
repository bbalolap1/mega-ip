"""Streamlit entry point for Mega IP Narrative Sandbox Version 0.0."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from app.branch_engine import create_branch
from app.canon_controller import is_selectable_canon_event, status_label
from app.character_engine import character_documents, find_ordos
from app.file_utils import list_markdown_files, read_text, write_text
from app.lore_parser import load_lore_documents, parse_markdown_file, split_frontmatter, validate_frontmatter
from app.scene_engine import first_scene, frontmatter_list
from app.timeline_engine import get_main_timeline, timeline_steps
from app.universe_navigator import universe_documents

ROOT = Path(__file__).parent
LORE_ROOT = ROOT / "lore"
BRANCHES_ROOT = ROOT / "branches"


@st.cache_data(show_spinner=False)
def cached_lore() -> list:
    return load_lore_documents(LORE_ROOT)


def refresh_lore() -> None:
    cached_lore.clear()


def status_badge(status: str) -> None:
    st.caption(f"Canon status: **{status_label(status)}**")


def page_universe(documents: list) -> None:
    st.title("Universe")
    st.write("Explore the first readable map of the Mega IP cosmology. No 3D is required for Version 0.0.")

    fixed_cards = [
        ("Prime Reality", "Highest named reality layer for Version 0.0; full structure unresolved."),
        ("Omniverse", "Largest navigable scale in the current foundation."),
        ("Nana", "Important world where Ordos' first divine decision occurs."),
        ("Abyss", "Opposing cosmological force and philosophy of domination/endless consumption."),
        ("Divine realms", "Important divine structures; completed form remains unresolved."),
        ("Important worlds", "World-level entries loaded from Markdown lore."),
    ]
    cols = st.columns(2)
    for index, (title, text) in enumerate(fixed_cards):
        with cols[index % 2].container(border=True):
            st.subheader(title)
            st.write(text)

    st.header("Loaded cosmology and world lore")
    for doc in universe_documents(documents):
        with st.expander(f"{doc.name} — {status_label(doc.status)}", expanded=doc.name in {"Nana", "Omniverse", "Abyss"}):
            st.markdown(doc.body)
            if doc.frontmatter:
                st.json(doc.frontmatter, expanded=False)


def page_chronicle(documents: list) -> None:
    st.title("Chronicle")
    st.write("Ordos' current narrative progression as an ordered timeline.")
    timeline = get_main_timeline(documents)
    steps = timeline_steps(timeline)
    if not steps:
        st.error("No valid Ordos main timeline found.")
        return
    for step in steps:
        with st.expander(f"{step['order']}. {step['title']} — {status_label(step['status'])}"):
            st.write(step["summary"])
            if step["status"] == "unresolved":
                st.warning("This transformation or detail is intentionally unresolved.")


def page_characters(documents: list) -> None:
    st.title("Characters")
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
    cols = st.columns(2)
    fields = [
        ("Identity", frontmatter.get("name")),
        ("Origin", frontmatter.get("origin")),
        ("Classification", frontmatter.get("classification")),
        ("Current domain", frontmatter.get("current_domain") or frontmatter.get("primary_domain")),
        ("Authority", frontmatter.get("authority")),
        ("Philosophy", frontmatter.get("philosophy")),
    ]
    for index, (label, value) in enumerate(fields):
        with cols[index % 2].container(border=True):
            st.caption(label)
            st.write(value or "Unresolved")
    st.subheader("Beliefs")
    for belief in frontmatter.get("beliefs", []):
        st.write(f"- {belief}")
    st.subheader("Linked events")
    for event in frontmatter.get("linked_events", []):
        st.write(f"- `{event}`")
    st.subheader("Unresolved questions")
    for question in frontmatter.get("unresolved_questions", []):
        st.warning(question)
    st.markdown(selected.body)


def page_lore_editor() -> None:
    st.title("Lore Editor")
    st.write("Edit Markdown lore only through an explicit save action. No autosave is used.")
    files = list_markdown_files(LORE_ROOT)
    choices = {path.relative_to(ROOT).as_posix(): path for path in files}
    selected_label = st.selectbox("Markdown file", list(choices))
    selected_path = choices[selected_label]
    raw_content = read_text(selected_path, LORE_ROOT)
    edited = st.text_area("Raw Markdown", value=raw_content, height=520)
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
    st.title("Scene Viewer")
    scene = first_scene(documents)
    if scene is None:
        st.error("The first scene is missing.")
        return
    st.header(scene.name)
    status_badge(scene.status)
    st.info(f"Setting: {scene.frontmatter.get('setting', 'Unresolved')}")
    st.subheader("Characters")
    st.write(", ".join(frontmatter_list(scene, "characters")))
    tabs = st.tabs(["Beats", "Narration", "Provisional Dialogue", "Consequences"])
    for tab, key in zip(tabs, ["beats", "narration", "provisional_dialogue", "consequences"]):
        with tab:
            for item in frontmatter_list(scene, key):
                st.container(border=True).write(item)
    st.markdown(scene.body)


def page_branch_creator(documents: list) -> None:
    st.title("Branch Creator")
    st.write("Create alternatives or experiments without overwriting canon Markdown.")
    events = [doc for doc in documents if is_selectable_canon_event(doc)]
    if not events:
        st.error("No canon events are available for branching.")
        return
    event_labels = {f"{doc.name} ({doc.id})": doc for doc in events}
    selected_label = st.selectbox("Source canon event", list(event_labels))
    branch_name = st.text_input("Branch name")
    branch_type = st.radio("Branch type", ["alternative", "experiment"], horizontal=True)
    changed_premise = st.text_area("Changed premise", height=180)
    if st.button("Save branch separately", type="primary"):
        try:
            record = create_branch(
                event_labels[selected_label], branch_name, branch_type, changed_premise, BRANCHES_ROOT
            )
            st.success(f"Created branch {record.branch_id} at {record.path.relative_to(ROOT)}.")
            st.info("The source canon event file was not overwritten.")
        except Exception as exc:
            st.error(f"Could not create branch: {exc}")


def main() -> None:
    st.set_page_config(page_title="Mega IP Narrative Sandbox", layout="wide")
    st.sidebar.title("Mega IP Narrative Sandbox")
    st.sidebar.caption("Version 0.0")
    page = st.sidebar.radio(
        "Navigate",
        ["Universe", "Chronicle", "Characters", "Lore Editor", "Scene Viewer", "Branch Creator"],
    )
    documents = cached_lore()
    invalid = [doc for doc in documents if not doc.is_valid]
    if invalid:
        st.sidebar.error(f"{len(invalid)} lore file(s) have validation errors.")
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

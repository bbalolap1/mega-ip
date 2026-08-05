from pathlib import Path

from app.branch_engine import create_branch
from app.lore_parser import parse_markdown_file


def test_branch_creation_does_not_overwrite_canon(tmp_path: Path) -> None:
    canon_path = tmp_path / "canon-event.md"
    canon_text = (
        "---\n"
        "id: event.test\n"
        "type: event\n"
        "status: canon\n"
        "name: Canon Test Event\n"
        "---\n\n"
        "# Canon Test Event\n\nOriginal canon text.\n"
    )
    canon_path.write_text(canon_text, encoding="utf-8")
    source_event = parse_markdown_file(canon_path)

    record = create_branch(
        source_event=source_event,
        branch_name="Shadow Imprisoned",
        branch_type="alternative",
        changed_premise="Ordos imprisons the shadow instead of removing it.",
        branches_root=tmp_path / "branches",
    )

    assert canon_path.read_text(encoding="utf-8") == canon_text
    assert record.path.exists()
    branch_text = record.path.read_text(encoding="utf-8")
    assert "source_event_id: event.test" in branch_text
    assert "Ordos imprisons the shadow" in branch_text
    assert record.path.parent.name == "alternatives"


def test_branch_creation_rejects_non_canon_source(tmp_path: Path) -> None:
    event_path = tmp_path / "event.md"
    event_path.write_text(
        "---\nid: event.alt\ntype: event\nstatus: provisional\nname: Provisional Event\n---\n\nBody\n",
        encoding="utf-8",
    )
    source_event = parse_markdown_file(event_path)

    try:
        create_branch(source_event, "Name", "alternative", "Premise", tmp_path / "branches")
    except ValueError as exc:
        assert "canon event" in str(exc)
    else:
        raise AssertionError("Expected non-canon source to be rejected")

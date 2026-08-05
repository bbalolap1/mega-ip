from pathlib import Path

from app.lore_parser import load_lore_documents, parse_markdown_file, split_frontmatter


def test_split_frontmatter_returns_yaml_and_body() -> None:
    raw = "---\nid: test.item\ntype: event\nstatus: canon\nname: Test Item\n---\n\n# Body\n"
    frontmatter, body = split_frontmatter(raw)
    assert frontmatter["id"] == "test.item"
    assert frontmatter["status"] == "canon"
    assert "# Body" in body


def test_invalid_status_is_reported(tmp_path: Path) -> None:
    path = tmp_path / "bad.md"
    path.write_text(
        "---\nid: bad.item\ntype: event\nstatus: official\nname: Bad Item\n---\n\nBody\n",
        encoding="utf-8",
    )
    document = parse_markdown_file(path)
    assert not document.is_valid
    assert "Invalid status" in document.errors[0]


def test_initial_lore_loads_without_validation_errors() -> None:
    documents = load_lore_documents(Path("lore"))
    assert documents
    assert all(document.is_valid for document in documents)
    assert {document.id for document in documents} >= {
        "character.ordos",
        "world.nana",
        "cosmology.omniverse",
        "world.abyss",
        "scene.ordos-first-divine-decision",
    }

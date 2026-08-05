"""Reusable Markdown + YAML frontmatter parser for lore files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - only used when dependencies are unavailable.
    from app import simple_yaml as yaml

from app.models import CANON_STATUSES, LoreDocument, REQUIRED_FRONTMATTER_FIELDS


class LoreParserError(ValueError):
    """Raised when a lore file cannot be parsed or validated."""


def split_frontmatter(raw_text: str) -> tuple[dict[str, Any], str]:
    """Separate YAML frontmatter from Markdown body.

    The parser intentionally stays small and readable. A lore file must begin
    with a YAML block delimited by `---` so the app can validate canon status.
    """
    if not raw_text.startswith("---\n"):
        raise LoreParserError("Markdown file must start with YAML frontmatter delimited by '---'.")

    parts = raw_text.split("---\n", 2)
    if len(parts) < 3:
        raise LoreParserError("Markdown file is missing a closing '---' frontmatter delimiter.")

    yaml_text = parts[1]
    body = parts[2].lstrip("\n")
    try:
        frontmatter = yaml.safe_load(yaml_text) or {}
    except Exception as exc:
        raise LoreParserError(f"Invalid YAML frontmatter: {exc}") from exc

    if not isinstance(frontmatter, dict):
        raise LoreParserError("YAML frontmatter must be a mapping of fields.")
    return frontmatter, body


def validate_frontmatter(frontmatter: dict[str, Any]) -> list[str]:
    """Return readable validation errors for required lore metadata."""
    errors: list[str] = []
    missing = sorted(REQUIRED_FRONTMATTER_FIELDS - set(frontmatter))
    if missing:
        errors.append(f"Missing required field(s): {', '.join(missing)}.")

    status = str(frontmatter.get("status", ""))
    if status and status not in CANON_STATUSES:
        errors.append(
            f"Invalid status '{status}'. Use one of: {', '.join(sorted(CANON_STATUSES))}."
        )

    for key in REQUIRED_FRONTMATTER_FIELDS:
        if key in frontmatter and not str(frontmatter[key]).strip():
            errors.append(f"Field '{key}' cannot be empty.")
    return errors


def parse_markdown_file(path: Path) -> LoreDocument:
    """Parse one Markdown lore file and include readable errors in the result."""
    try:
        raw_text = path.read_text(encoding="utf-8")
        frontmatter, body = split_frontmatter(raw_text)
        errors = validate_frontmatter(frontmatter)
        return LoreDocument(path=path, frontmatter=frontmatter, body=body, errors=errors)
    except (OSError, LoreParserError) as exc:
        return LoreDocument(path=path, frontmatter={}, body="", errors=[str(exc)])


def load_lore_documents(lore_root: Path) -> list[LoreDocument]:
    """Load all Markdown lore files beneath the lore directory."""
    documents = [parse_markdown_file(path) for path in sorted(lore_root.rglob("*.md"))]
    return [doc for doc in documents if doc.status != "removed"]


def documents_by_type(documents: list[LoreDocument], lore_type: str) -> list[LoreDocument]:
    """Filter valid documents by frontmatter type."""
    return [doc for doc in documents if doc.is_valid and doc.type == lore_type]

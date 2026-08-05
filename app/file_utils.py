"""Safe file helpers for the Streamlit app."""

from __future__ import annotations

from pathlib import Path


def list_markdown_files(root: Path) -> list[Path]:
    """Return Markdown files under a root, sorted for stable UI display."""
    return sorted(root.rglob("*.md"))


def ensure_inside_root(path: Path, root: Path) -> None:
    """Raise an error if `path` escapes `root` after resolving symlinks."""
    resolved_path = path.resolve()
    resolved_root = root.resolve()
    if resolved_root not in resolved_path.parents and resolved_path != resolved_root:
        raise ValueError(f"Refusing to write outside {resolved_root}.")


def read_text(path: Path, root: Path) -> str:
    ensure_inside_root(path, root)
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str, root: Path) -> None:
    ensure_inside_root(path, root)
    path.write_text(content, encoding="utf-8")

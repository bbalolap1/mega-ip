"""Small typed models for lore loaded from Markdown."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

CANON_STATUSES = {
    "canon",
    "provisional",
    "unresolved",
    "alternative",
    "experiment",
    "archived",
    "removed",
}

REQUIRED_FRONTMATTER_FIELDS = {"id", "type", "status", "name"}


@dataclass(frozen=True)
class LoreDocument:
    """A parsed Markdown lore document with validated frontmatter."""

    path: Path
    frontmatter: dict[str, Any]
    body: str
    errors: list[str] = field(default_factory=list)

    @property
    def id(self) -> str:
        return str(self.frontmatter.get("id", ""))

    @property
    def type(self) -> str:
        return str(self.frontmatter.get("type", ""))

    @property
    def status(self) -> str:
        return str(self.frontmatter.get("status", ""))

    @property
    def name(self) -> str:
        return str(self.frontmatter.get("name", self.path.stem))

    @property
    def is_valid(self) -> bool:
        return not self.errors


@dataclass(frozen=True)
class BranchRecord:
    """Metadata returned after safely writing a non-canon branch file."""

    path: Path
    branch_id: str
    source_event_id: str
    branch_type: str

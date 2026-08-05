"""Presentation helpers that keep Streamlit pages readable and lore-focused."""

from __future__ import annotations

from app.models import LoreDocument

STATUS_TONES = {
    "canon": "stable canon",
    "provisional": "usable, unsettled",
    "unresolved": "do not complete by invention",
    "alternative": "separate branch",
    "experiment": "temporary branch",
    "archived": "inactive archive",
    "removed": "hidden from active views",
}


def status_tone(status: str) -> str:
    """Explain a canon status in creator-facing language."""
    return STATUS_TONES.get(status, "unknown status")


def lore_counts(documents: list[LoreDocument]) -> dict[str, int]:
    """Count valid lore documents by type for the sidebar snapshot."""
    counts: dict[str, int] = {}
    for document in documents:
        if document.is_valid:
            counts[document.type] = counts.get(document.type, 0) + 1
    return counts


def timeline_stage(order: int) -> str:
    """Group Ordos' timeline into readable narrative arcs without changing lore."""
    if order <= 4:
        return "Earth origin"
    if order <= 9:
        return "Divine awakening"
    if order <= 14:
        return "Civilization and cultivation"
    return "Unsettled horizon"

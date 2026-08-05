"""Helpers for canon status handling."""

from __future__ import annotations

from app.models import CANON_STATUSES, LoreDocument


def status_label(status: str) -> str:
    labels = {
        "canon": "Canon",
        "provisional": "Provisional",
        "unresolved": "Unresolved",
        "alternative": "Alternative",
        "experiment": "Experiment",
        "archived": "Archived",
        "removed": "Removed",
    }
    return labels.get(status, status or "Unknown")


def is_selectable_canon_event(document: LoreDocument) -> bool:
    return document.is_valid and document.type == "event" and document.status == "canon"


def validate_status(status: str) -> bool:
    return status in CANON_STATUSES

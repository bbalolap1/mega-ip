"""Timeline helpers for Ordos' chronicle."""

from __future__ import annotations

from app.models import LoreDocument


def get_main_timeline(documents: list[LoreDocument]) -> LoreDocument | None:
    for doc in documents:
        if doc.id == "timeline.ordos.main":
            return doc
    return None


def timeline_steps(document: LoreDocument | None) -> list[dict[str, str]]:
    if document is None:
        return []
    steps = document.frontmatter.get("steps", [])
    if not isinstance(steps, list):
        return []
    normalized: list[dict[str, str]] = []
    for index, item in enumerate(steps, start=1):
        if isinstance(item, dict):
            normalized.append(
                {
                    "order": str(item.get("order", index)),
                    "title": str(item.get("title", "Untitled step")),
                    "status": str(item.get("status", document.status)),
                    "summary": str(item.get("summary", "")),
                }
            )
    return normalized

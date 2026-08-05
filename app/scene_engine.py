"""Scene viewer helpers."""

from __future__ import annotations

from app.models import LoreDocument


def first_scene(documents: list[LoreDocument]) -> LoreDocument | None:
    for doc in documents:
        if doc.id == "scene.ordos-first-divine-decision":
            return doc
    return None


def frontmatter_list(document: LoreDocument, key: str) -> list[str]:
    value = document.frontmatter.get(key, [])
    if isinstance(value, list):
        return [str(item) for item in value]
    return []

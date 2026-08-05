"""Universe page data helpers."""

from __future__ import annotations

from app.models import LoreDocument


def universe_documents(documents: list[LoreDocument]) -> list[LoreDocument]:
    wanted_types = {"cosmology", "world", "realm"}
    wanted_names = {"Prime Reality", "Omniverse", "Nana", "Abyss"}
    return [
        doc
        for doc in documents
        if doc.is_valid and (doc.type in wanted_types or doc.name in wanted_names)
    ]

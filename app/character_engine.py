"""Character page data helpers."""

from __future__ import annotations

from app.models import LoreDocument


def character_documents(documents: list[LoreDocument]) -> list[LoreDocument]:
    return [doc for doc in documents if doc.is_valid and doc.type == "character"]


def find_ordos(documents: list[LoreDocument]) -> LoreDocument | None:
    for doc in character_documents(documents):
        if doc.id == "character.ordos":
            return doc
    return None

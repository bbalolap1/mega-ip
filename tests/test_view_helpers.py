from pathlib import Path

from app.models import LoreDocument
from app.view_helpers import lore_counts, status_tone, timeline_stage


def test_timeline_stage_groups_progression_without_changing_lore() -> None:
    assert timeline_stage(1) == "Earth origin"
    assert timeline_stage(8) == "Divine awakening"
    assert timeline_stage(12) == "Civilization and cultivation"
    assert timeline_stage(18) == "Unsettled horizon"


def test_lore_counts_only_counts_valid_documents() -> None:
    documents = [
        LoreDocument(Path("a.md"), {"id": "a", "type": "character", "status": "canon", "name": "A"}, ""),
        LoreDocument(Path("b.md"), {"id": "b", "type": "event", "status": "canon", "name": "B"}, ""),
        LoreDocument(Path("bad.md"), {}, "", ["invalid"]),
    ]
    assert lore_counts(documents) == {"character": 1, "event": 1}


def test_status_tone_explains_unresolved_boundary() -> None:
    assert status_tone("unresolved") == "do not complete by invention"

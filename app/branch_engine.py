"""Branch creation with explicit canon-file safety."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import re

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - only used when dependencies are unavailable.
    from app import simple_yaml as yaml

from app.file_utils import ensure_inside_root
from app.models import BranchRecord, LoreDocument


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "untitled-branch"


def create_branch(
    source_event: LoreDocument,
    branch_name: str,
    branch_type: str,
    changed_premise: str,
    branches_root: Path,
) -> BranchRecord:
    """Create an alternative or experiment branch without touching canon lore."""
    if source_event.type != "event" or source_event.status != "canon":
        raise ValueError("Branches can only be created from canon event documents.")
    if branch_type not in {"alternative", "experiment"}:
        raise ValueError("Branch type must be 'alternative' or 'experiment'.")
    if not branch_name.strip():
        raise ValueError("Branch name is required.")
    if not changed_premise.strip():
        raise ValueError("Changed premise is required.")

    target_dir = branches_root / f"{branch_type}s"
    target_dir.mkdir(parents=True, exist_ok=True)
    ensure_inside_root(target_dir, branches_root)

    branch_slug = slugify(branch_name)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    target_path = target_dir / f"{branch_slug}-{timestamp}.md"
    ensure_inside_root(target_path, branches_root)

    frontmatter = {
        "id": f"branch.{branch_type}.{branch_slug}",
        "type": "branch",
        "status": branch_type,
        "name": branch_name.strip(),
        "source_event_id": source_event.id,
        "source_event_name": source_event.name,
        "source_event_path": source_event.path.as_posix(),
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    body = (
        f"# {branch_name.strip()}\n\n"
        "## Source Canon Event\n\n"
        f"- `{source_event.id}` — {source_event.name}\n\n"
        "## Changed Premise\n\n"
        f"{changed_premise.strip()}\n\n"
        "## Safety Note\n\n"
        "This branch is stored separately and does not overwrite canon Markdown.\n"
    )
    content = "---\n" + yaml.safe_dump(frontmatter, sort_keys=False) + "---\n\n" + body
    target_path.write_text(content, encoding="utf-8")
    return BranchRecord(
        path=target_path,
        branch_id=str(frontmatter["id"]),
        source_event_id=source_event.id,
        branch_type=branch_type,
    )

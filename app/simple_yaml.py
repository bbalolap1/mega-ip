"""Tiny YAML fallback for the simple frontmatter used in Version 0.0.

PyYAML is the required runtime dependency. This fallback only keeps tests and
basic parser checks usable in restricted environments where dependencies cannot
be installed. It supports the small subset used by this repository: scalar
fields, lists of scalars, and lists of simple dictionaries.
"""

from __future__ import annotations

from typing import Any


def safe_load(text: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    current_key: str | None = None
    current_dict: dict[str, Any] | None = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            item_text = line[4:]
            if ":" in item_text:
                key, value = item_text.split(":", 1)
                current_dict = {key.strip(): _clean_scalar(value.strip())}
                result.setdefault(current_key, []).append(current_dict)
            else:
                current_dict = None
                result.setdefault(current_key, []).append(_clean_scalar(item_text))
            continue
        if line.startswith("    ") and current_dict is not None and ":" in line:
            key, value = line.strip().split(":", 1)
            current_dict[key.strip()] = _clean_scalar(value.strip())
            continue
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_dict = None
            if value:
                result[key] = _clean_scalar(value)
                current_key = None
            else:
                result[key] = []
                current_key = key
    return result


def safe_dump(data: dict[str, Any], sort_keys: bool = False) -> str:
    items = sorted(data.items()) if sort_keys else data.items()
    lines: list[str] = []
    for key, value in items:
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                if isinstance(item, dict):
                    first = True
                    for subkey, subvalue in item.items():
                        prefix = "  - " if first else "    "
                        lines.append(f"{prefix}{subkey}: {_format_scalar(subvalue)}")
                        first = False
                else:
                    lines.append(f"  - {_format_scalar(item)}")
        else:
            lines.append(f"{key}: {_format_scalar(value)}")
    return "\n".join(lines) + "\n"


def _clean_scalar(value: str) -> Any:
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    if value.isdigit():
        return int(value)
    return value


def _format_scalar(value: Any) -> str:
    text = str(value)
    if ":" in text or text.startswith("[") or text.startswith("{"):
        return repr(text)
    return text

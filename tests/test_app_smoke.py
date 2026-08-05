from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path


def test_app_exposes_required_navigation_without_real_streamlit() -> None:
    """Smoke-test app wiring when Streamlit cannot be installed in CI.

    The real application still requires Streamlit at runtime. This fake module
    lets us verify the required page list and repository paths without turning
    tests into a Streamlit integration suite.
    """
    fake_streamlit = types.ModuleType("streamlit")
    fake_streamlit.cache_data = lambda show_spinner=False: (lambda func: func)
    sys.modules["streamlit"] = fake_streamlit
    try:
        spec = importlib.util.spec_from_file_location("mega_ip_streamlit_app", Path("app.py"))
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop("streamlit", None)

    assert module.PAGES == [
        "Universe",
        "Chronicle",
        "Characters",
        "Lore Editor",
        "Scene Viewer",
        "Branch Creator",
    ]
    assert module.LORE_ROOT.name == "lore"
    assert module.BRANCHES_ROOT.name == "branches"

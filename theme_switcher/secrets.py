# theme_switcher/secrets.py
import streamlit as st

def _get_secret(key, default=None):
    try:
        return st.secrets.get(key, default)
    except Exception:
        return default

def is_switcher_allowed() -> bool:
    val = _get_secret("allow_theme_switch", True)
    if isinstance(val, bool):
        return val
    return str(val).strip().lower() == "true"

def get_ui_location() -> str:
    val = str(_get_secret("theme_ui_location", "sidebar")).strip().lower()
    return val if val in ("sidebar", "header", "footer") else "sidebar"

def get_selector_style() -> str:
    val = str(_get_secret("theme_selector_style", "icons")).strip().lower()
    return val if val in ("icons", "dropdown") else "icons"

def get_themes_metadata() -> dict:
    # supports [themes.<stem>] tables, or missing
    try:
        themes = st.secrets.get("themes", {})
        return themes if isinstance(themes, dict) else {}
    except Exception:
        return {}
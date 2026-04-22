# theme_switcher/api.py
import streamlit as st
from .switcher import ThemeSwitcher
from .secrets import get_ui_location

def quick_theme_setup(default_theme="rose_gold", themes_dir="themes", key_prefix="theme_switcher"):
    return apply_theme(
        default_theme=default_theme,
        themes_dir=themes_dir,
        show_selector=True,
        allow_customization=False,
        key_prefix=key_prefix,
    )

def apply_theme(
    default_theme="rose_gold",
    themes_dir="themes",
    show_selector=True,
    allow_customization=False,
    selector_location=None,
    key_prefix="theme_switcher",
):
    """
    One call to apply theme CSS and render selector.
    Default UI location is footer if no secrets exist.
    """
    ts_key = f"_ts_instance_{key_prefix}"
    ts = ThemeSwitcher(default_theme=default_theme, themes_dir=themes_dir, key_prefix=key_prefix)
    st.session_state[ts_key] = ts

    location = selector_location or get_ui_location()

    ts.apply_theme()

    if show_selector:
        ts.render_selector(location=location)

    ts.maybe_add_customization(enable=allow_customization, location=location)
    return ts
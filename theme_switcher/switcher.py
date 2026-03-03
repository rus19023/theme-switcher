# theme_switcher/switcher.py

import streamlit as st
from pathlib import Path

from .secrets import is_switcher_allowed, get_ui_location, get_themes_metadata
from .discovery import discover_themes
from .loader import load_base_css, load_theme_css
from .css_inject import (
    inject_icon_button_css,
    inject_tooltip_css,
    inject_combined_css,
    inject_font_links,
    inject_sticky_bar_css,
)
from .customize import add_customization_controls


class ThemeSwitcher:
    def __init__(self, default_theme="rose_gold", themes_dir="themes", key_prefix="theme_switcher"):
        themes_path = Path(themes_dir)
        if not themes_path.is_absolute():
            if themes_path.exists():
                self.themes_dir = themes_path
            else:
                self.themes_dir = Path(__file__).parent / themes_dir
        else:
            self.themes_dir = themes_path

        self.default_theme = default_theme
        self.key_prefix = key_prefix

        # Discover themes every run so new CSS files show up
        secrets_meta_raw = get_themes_metadata()
        self.available_themes = discover_themes(self.themes_dir, secrets_meta=secrets_meta_raw)

        theme_state_key = f"{self.key_prefix}_current_theme"
        if theme_state_key not in st.session_state:
            if default_theme in self.available_themes:
                st.session_state[theme_state_key] = default_theme
            else:
                st.session_state[theme_state_key] = next(iter(self.available_themes.keys()), default_theme)

    def render_selector(self, title="Theme", location="sidebar", show_description=True):
        if not is_switcher_allowed():
            return

        resolved_location = location or get_ui_location()

        if resolved_location == "sidebar":
            self._render_sidebar(title, show_description)
        elif resolved_location == "header":
            self._render_inline(title, position="header")
        elif resolved_location == "footer":
            self._render_inline(title, position="footer")

    def _render_sidebar(self, title, show_description):
        theme_state_key = f"{self.key_prefix}_current_theme"
        current_theme = st.session_state.get(theme_state_key, self.default_theme)
        current_icon = self.available_themes.get(current_theme, {}).get("icon", "🎨")

        with st.sidebar:
            inject_icon_button_css()
            inject_tooltip_css()

            with st.expander(f"{current_icon} {title}", expanded=False):
                keys = list(self.available_themes.keys())
                self._render_icon_button_grid(keys, theme_state_key, cols_per_row=5)

            if show_description and current_theme in self.available_themes:
                desc = self.available_themes[current_theme].get("description", "")
                if desc:
                    st.caption(f"_{desc}_")

            # Image credit — only shown when theme has a background image credit
            credit = st.session_state.get(f"{self.key_prefix}_image_credit")
            if credit:
                st.markdown(f"<small>📷 {credit}</small>", unsafe_allow_html=True)

    def _render_inline(self, title, position: str):
        theme_state_key = f"{self.key_prefix}_current_theme"
        inject_icon_button_css()
        inject_tooltip_css()
        inject_sticky_bar_css(position)

        st.markdown(f'<div class="theme-bar"><span class="bar-label">🎨 {title}</span></div>', unsafe_allow_html=True)

        keys = list(self.available_themes.keys())
        self._render_icon_button_grid(keys, theme_state_key, cols_per_row=max(1, len(keys)))

    def _render_icon_button_grid(self, theme_keys, theme_state_key, cols_per_row=5):
        if not theme_keys:
            st.caption("No themes found.")
            return

        rows = [theme_keys[i:i + cols_per_row] for i in range(0, len(theme_keys), cols_per_row)]
        for row in rows:
            cols = st.columns(cols_per_row)
            for i, col in enumerate(cols):
                with col:
                    if i >= len(row):
                        st.write("")
                        continue

                    key = row[i]
                    data = self.available_themes[key]
                    is_active = st.session_state.get(theme_state_key) == key
                    label = f"{'▶' if is_active else ''}{data.get('icon', '🎨')}"

                    if st.button(
                        label,
                        key=f"{self.key_prefix}_icon_{key}",
                        help=data.get("name", key),
                        use_container_width=True,
                    ):
                        if st.session_state.get(theme_state_key) != key:
                            st.session_state[theme_state_key] = key
                            st.rerun()

    def apply_theme(self):
        theme_state_key = f"{self.key_prefix}_current_theme"
        theme_key = st.session_state.get(theme_state_key, self.default_theme)
        theme_data = self.available_themes.get(theme_key)

        if not theme_data:
            st.warning(f"Theme '{theme_key}' not found.")
            return

        base_css_file = self.themes_dir / "theme_base.css"
        base_css = load_base_css(base_css_file)

        images_dir = self.themes_dir / "images"
        theme_css_file = self.themes_dir / theme_data["css_file"]
        theme_css, font_urls, meta = load_theme_css(theme_css_file, images_dir=images_dir)

        inject_font_links(font_urls)
        inject_combined_css(base_css, theme_css)

        # Store image credit in session state for sidebar to render
        st.session_state[f"{self.key_prefix}_image_credit"] = meta.get("image_credit")

    def maybe_add_customization(self, enable: bool, location: str):
        if not enable:
            return
        container = st.sidebar if location == "sidebar" else st
        add_customization_controls(container)

        
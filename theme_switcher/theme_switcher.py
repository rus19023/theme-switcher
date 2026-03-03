# """
# theme_switcher.py

# Modular Theme Switcher for Streamlit

"""
theme_switcher.py

Thin wrapper that re-exports the modular package API.
"""

from theme_switcher.api import apply_theme, quick_theme_setup
from theme_switcher.switcher import ThemeSwitcher

__all__ = ["apply_theme", "quick_theme_setup", "ThemeSwitcher"]


# A drop-in solution for adding professional themes to any Streamlit app.
# Supports both built-in themes (from THEMES dict) and custom themes (CSS files in /themes directory).

# Secrets-controlled behavior (in .streamlit/secrets.toml):

#     allow_theme_switch = true        # Show or hide the theme switcher UI (default: true)
#     theme_ui_location = "sidebar"    # Where to show it: "sidebar", "header", or "footer"
# """

# import streamlit as st
# from pathlib import Path
# import re


# def _get_secret(key, default=None):
#     """Safely read a value from st.secrets, returning default if missing."""
#     try:
#         return st.secrets[key]
#     except (KeyError, FileNotFoundError):
#         return default


# class ThemeSwitcher:
#     """
#     Manages theme switching in Streamlit apps.

#     Themes are discovered automatically by scanning the themes directory.
#     Metadata (name, icon, description) is read from st.secrets:

#         [themes.mytheme]
#         name = "My Theme"
#         icon = "🌊"
#         description = "A cool ocean theme"

#     To add a new theme: add its metadata to secrets.toml and drop the
#     CSS file into the themes/ folder. No Python changes needed.
#     Themes without a secrets entry will still appear with a 🎨 icon
#     and an auto-generated name from the filename.

#     Usage:
#         ts = ThemeSwitcher(default_theme='retro')
#         ts.render_selector()  # Shows theme switcher (location controlled by secrets)
#         ts.apply_theme()      # Applies the selected theme

#     Secrets (in .streamlit/secrets.toml):
#         allow_theme_switch = true
#         theme_ui_location = "sidebar"   # "sidebar" | "header" | "footer"
#     """

#     # Theme metadata is read automatically from each CSS file's header comment.
#     # Add these tags to any theme CSS to register it — no Python changes needed:
#     #
#     #   /*
#     #      filename.css
#     #      @theme-name: My Theme
#     #      @theme-icon: 🎨
#     #      @theme-description: Short description
#     #   */

#     def __init__(self, default_theme='rose_gold', themes_dir='themes', key_prefix='theme_switcher'):
#         """
#         Initialize the theme switcher.

#         Args:
#             default_theme: Theme key to use by default
#             themes_dir: Directory containing CSS theme files (relative to caller or absolute)
#             key_prefix: Unique prefix for widget keys to prevent conflicts
#         """
#         themes_path = Path(themes_dir)
#         if not themes_path.is_absolute():
#             if themes_path.exists():
#                 self.themes_dir = themes_path
#             else:
#                 self.themes_dir = Path(__file__).parent / themes_dir
#         else:
#             self.themes_dir = themes_path

#         self.default_theme = default_theme
#         self.key_prefix = key_prefix

#         self.available_themes = self._discover_themes()

#         theme_state_key = f'{self.key_prefix}_current_theme'
#         if theme_state_key not in st.session_state:
#             st.session_state[theme_state_key] = (
#                 default_theme if default_theme in self.available_themes
#                 else list(self.available_themes.keys())[0]
#             )

#     @staticmethod
#     def _get_secrets_metadata():
#         """
#         Read theme metadata from st.secrets[themes] if present.

#         Expected format in .streamlit/secrets.toml:

#             [themes.neon]
#             name = "Neon Nights"
#             icon = "🌃"
#             description = "Vibrant nightlife energy"

#             [themes.retro]
#             name = "Retro Gaming"
#             icon = "🕹️"
#             description = "8-bit nostalgia"

#         Returns a dict keyed by theme stem (filename without .css).
#         """
#         try:
#             themes_secret = st.secrets.get("themes", {})
#             result = {}
#             for key, data in themes_secret.items():
#                 result[key] = {
#                     'name': data.get('name', key.replace('_', ' ').title()),
#                     'icon': data.get('icon', '🎨'),
#                     'description': data.get('description', ''),
#                 }
#             return result
#         except Exception:
#             return {}


#     def _discover_themes(self):
#         """
#         Discover all available themes by scanning the themes directory.

#         Metadata priority:
#           1. st.secrets[themes.<name>] — name, icon, description
#           2. Auto-generated from filename as fallback

#         To register a theme, add to .streamlit/secrets.toml:

#             [themes.mytheme]
#             name = "My Theme"
#             icon = "🌊"
#             description = "A cool ocean theme"

#         Then drop mytheme.css into the themes/ folder. No Python changes needed.
#         """
#         available = {}

#         if not self.themes_dir.exists():
#             return available

#         secrets_meta = self._get_secrets_metadata()

#         for css_file in sorted(self.themes_dir.glob("*.css")):
#             if css_file.stem in ['theme_base', 'theme_template']:
#                 continue

#             stem = css_file.stem
#             meta = secrets_meta.get(stem, {})

#             available[stem] = {
#                 'name': meta.get('name', stem.replace('_', ' ').title()),
#                 'icon': meta.get('icon', '🎨'),
#                 'description': meta.get('description', ''),
#                 'source': 'built-in' if meta else 'custom',
#                 'css_file': css_file.name,
#             }

#         return available

#     # ------------------------------------------------------------------
#     # SECRETS HELPERS
#     # ------------------------------------------------------------------

#     @staticmethod
#     def _is_switcher_allowed():
#         """Check st.secrets for allow_theme_switch. Defaults to True if not set."""
#         val = _get_secret('allow_theme_switch', default=True)
#         # Accept both bool True and string "true"
#         if isinstance(val, bool):
#             return val
#         return str(val).strip().lower() == 'true'


#     @staticmethod
#     def _get_ui_location():
#         """
#         Read theme_ui_location from st.secrets.
#         Valid values: 'sidebar', 'header', 'footer'
#         Defaults to 'sidebar'.
#         """
#         val = _get_secret('theme_ui_location', default='sidebar')
#         val = str(val).strip().lower()
#         if val in ('sidebar', 'header', 'footer'):
#             return val
#         return 'sidebar'

#     # ------------------------------------------------------------------
#     # RENDER SELECTOR
#     # ------------------------------------------------------------------

#     def render_selector(self, title="🎨 Theme", location=None, show_description=False):
#         """
#         Render the theme selector UI.

#         Location is determined by the secret 'theme_ui_location' unless
#         overridden by the location argument. If allow_theme_switch is False
#         in secrets, this method does nothing.

#         Args:
#             title: Label shown above the selector
#             location: Override location ('sidebar', 'header', 'footer').
#                       If None, reads from st.secrets['theme_ui_location'].
#             show_description: Show theme description below selector (sidebar only)
#         """
#         if not self._is_switcher_allowed():
#             return

#         resolved_location = location if location is not None else self._get_ui_location()

#         if resolved_location == 'sidebar':
#             self._render_icon_selector_sidebar(title, show_description)
#         elif resolved_location == 'header':
#             self._render_icon_selector_inline(title, position='header')
#         elif resolved_location == 'footer':
#             self._render_icon_selector_inline(title, position='footer')


#     def _render_icon_selector_sidebar(self, title, show_description):
#         """Render icon buttons in the sidebar inside an expander."""
#         theme_state_key = f'{self.key_prefix}_current_theme'
#         current_theme = st.session_state[theme_state_key]
#         current_icon = self.available_themes.get(current_theme, {}).get('icon', '🎨')

#         with st.sidebar:
#             self._inject_icon_button_css()

#             with st.expander(f"{current_icon} {title}", expanded=False):
#                 # Split built-in vs custom themes
#                 builtin_keys = [k for k, v in self.available_themes.items() if v.get('source') == 'built-in']
#                 custom_keys = [k for k, v in self.available_themes.items() if v.get('source') == 'custom']

#                 self._render_icon_button_row(builtin_keys, theme_state_key)

#                 if custom_keys:
#                     st.caption("Custom themes")
#                     self._render_icon_button_row(custom_keys, theme_state_key)

#             if show_description:
#                 theme_data = self.available_themes[current_theme]
#                 st.caption(f"_{theme_data['description']}_")


#     def _render_icon_button_row(self, theme_keys, theme_state_key, cols_per_row=5):
#         """Render a grid of icon buttons for the given theme keys."""
#         rows = [theme_keys[i:i + cols_per_row] for i in range(0, len(theme_keys), cols_per_row)]
#         for row in rows:
#             cols = st.columns(cols_per_row)
#             for i, col in enumerate(cols):
#                 with col:
#                     if i < len(row):
#                         key = row[i]
#                         data = self.available_themes[key]
#                         is_active = st.session_state[theme_state_key] == key
#                         label = f"{'▶' if is_active else ''}{data['icon']}"
#                         if st.button(
#                             label,
#                             key=f"{self.key_prefix}_icon_{key}",
#                             help=data['name'],
#                             use_container_width=True
#                         ):
#                             if st.session_state[theme_state_key] != key:
#                                 st.session_state[theme_state_key] = key
#                                 st.rerun()


#     def _render_icon_selector_inline(self, title, position):
#         """
#         Render icon buttons inline as a sticky header or footer bar
#         using fixed-position CSS injection.
#         """
#         theme_state_key = f'{self.key_prefix}_current_theme'
#         self._inject_icon_button_css()

#         if position == 'header':
#             css_position = "top: 0; left: 0; right: 0;"
#             padding_target = ".block-container { padding-top: 3.5rem !important; }"
#         else:
#             css_position = "bottom: 0; left: 0; right: 0;"
#             padding_target = ".block-container { padding-bottom: 3.5rem !important; }"

#         # Inject sticky bar CSS
#         st.markdown(f"""
#             <style>
#             .theme-bar {{
#                 position: fixed;
#                 {css_position}
#                 z-index: 9998;
#                 background: rgba(0,0,0,0.75);
#                 backdrop-filter: blur(8px);
#                 padding: 6px 16px;
#                 display: flex;
#                 align-items: center;
#                 gap: 8px;
#                 border-{'bottom' if position == 'header' else 'top'}: 1px solid rgba(255,255,255,0.1);
#             }}
#             .theme-bar span.bar-label {{
#                 font-size: 0.75rem;
#                 opacity: 0.6;
#                 margin-right: 4px;
#                 white-space: nowrap;
#             }}
#             {padding_target}
#             </style>
#         """, unsafe_allow_html=True)

#         # Render built-in themes first, custom themes after
#         builtin_keys = [k for k, v in self.available_themes.items() if v.get('source') == 'built-in']
#         custom_keys = [k for k, v in self.available_themes.items() if v.get('source') == 'custom']

#         st.markdown(f'<div style="margin-bottom:2px"><small>{title}</small></div>', unsafe_allow_html=True)
#         self._render_icon_button_row(builtin_keys, theme_state_key, cols_per_row=len(builtin_keys))
#         if custom_keys:
#             st.caption("Custom")
#             self._render_icon_button_row(custom_keys, theme_state_key, cols_per_row=len(custom_keys))

#     def _inject_icon_button_css(self):
#         #Inject compact styling for ONLY the theme icon buttons (not expander header).
#         st.markdown("""
#             <style>
#             /* Only target buttons INSIDE expander content (details), not the expander header button */
#             section[data-testid="stSidebar"]
#             div[data-testid="stExpander"]
#             div[data-testid="stExpanderDetails"]
#             div[data-testid="stHorizontalBlock"]
#             div[data-testid="column"]
#             div[data-testid="stButton"] > button {

#                 padding: 4px 2px !important;
#                 font-size: 1.2rem !important;
#                 min-height: unset !important;
#                 line-height: 1.3 !important;
#                 border-radius: 6px !important;
#                 background: var(--theme-bg-card, rgba(255,255,255,0.05)) !important;
#                 border: 1px solid var(--theme-border-color, rgba(255,255,255,0.15)) !important;
#                 color: inherit !important;
#                 box-shadow: none !important;
#             }

#             section[data-testid="stSidebar"]
#             div[data-testid="stExpander"]
#             div[data-testid="stExpanderDetails"]
#             div[data-testid="stHorizontalBlock"]
#             div[data-testid="column"]
#             div[data-testid="stButton"] > button:hover {

#                 background: var(--theme-bg-secondary, rgba(255,255,255,0.1)) !important;
#                 border-color: var(--theme-color-primary, rgba(255,255,255,0.4)) !important;
#                 transform: none !important;
#             }
#             </style>
#         """, unsafe_allow_html=True)
#     def _read_css_header_metadata(self, css_file: Path):
#         """
#         Parse optional header block like:

#         /*
#         @theme-name: Retro Gaming
#         @theme-icon: 🕹️
#         @theme-description: 8-bit nostalgia
#         */
#         """
#         try:
#             text = css_file.read_text(encoding="utf-8", errors="ignore")
#         except Exception:
#             return {}

#         # Only scan the first ~2KB for speed
#         head = text[:2048]

#         # Find first /* ... */ block
#         m = re.search(r"/\*([\s\S]*?)\*/", head)
#         if not m:
#             return {}

#         block = m.group(1)

#         def grab(tag):
#             mm = re.search(rf"@{tag}\s*:\s*(.+)", block, flags=re.IGNORECASE)
#             return mm.group(1).strip() if mm else None

#         return {
#             "name": grab("theme-name"),
#             "icon": grab("theme-icon"),
#             "description": grab("theme-description"),
#         }

#     # ------------------------------------------------------------------
#     # LEGACY DROPDOWN (still available if needed)
#     # ------------------------------------------------------------------

#     def render_dropdown_selector(self, title="🎨 Theme Selector", location='sidebar', show_description=False):
#         """
#         Render theme selection as a dropdown (legacy method).

#         Useful as a fallback or for admin panels.
#         Not affected by allow_theme_switch secret.
#         """
#         container = st.sidebar if location == 'sidebar' else st
#         theme_state_key = f'{self.key_prefix}_current_theme'

#         with container:
#             st.markdown(f"### {title}")
#             theme_options = {key: data['name'] for key, data in self.available_themes.items()}
#             theme_keys = list(theme_options.keys())
#             theme_labels = list(theme_options.values())

#             try:
#                 current_index = theme_keys.index(st.session_state[theme_state_key])
#             except (ValueError, KeyError):
#                 current_index = 0
#                 st.session_state[theme_state_key] = theme_keys[0]

#             selected_label = st.selectbox(
#                 "Choose a theme:",
#                 options=theme_labels,
#                 index=current_index,
#                 key=f"{self.key_prefix}_selector_dropdown"
#             )
#             selected_theme = theme_keys[theme_labels.index(selected_label)]

#             if st.session_state[theme_state_key] != selected_theme:
#                 st.session_state[theme_state_key] = selected_theme
#                 st.rerun()

#             if show_description:
#                 theme_data = self.available_themes[st.session_state[theme_state_key]]
#                 st.caption(f"_{theme_data['description']}_")

#     # ------------------------------------------------------------------
#     # APPLY THEME
#     # ------------------------------------------------------------------

#     def apply_theme(self):
#         """
#         Apply the currently selected theme by injecting CSS.

#         Loads:
#         1. theme_base.css
#         2. Theme-specific CSS
#         3. Google Fonts
#         """
#         theme_state_key = f'{self.key_prefix}_current_theme'
#         theme_key = st.session_state[theme_state_key]
#         theme_data = self.available_themes.get(theme_key)

#         if not theme_data:
#             st.error(f"Theme '{theme_key}' not found!")
#             return

#         base_css_content = self._load_base_css()
#         theme_css_content = self._load_theme_css(theme_data)
#         self._inject_fonts(theme_data)

#         combined_css = f"""
#             <style>
#             /* === RESET === */
#             * {{
#                 margin: 0;
#                 padding: 0;
#                 box-sizing: border-box;
#             }}

#             /* === BASE CSS === */
#             {base_css_content}

#             /* === THEME CSS === */
#             {theme_css_content}
#             </style>
#             """
#         st.markdown(combined_css, unsafe_allow_html=True)

#     def _load_base_css(self):
#         """Load the base CSS file if it exists."""
#         base_css_file = Path(__file__).parent / "theme_base.css"
#         if base_css_file.exists():
#             try:
#                 with open(base_css_file, 'r', encoding='utf-8') as f:
#                     return f.read()
#             except Exception as e:
#                 st.warning(f"Could not load theme_base.css: {e}")
#         return ""

#     def _load_theme_css(self, theme_data):
#         """Load the theme-specific CSS file."""
#         css_file = self.themes_dir / theme_data['css_file']

#         if not css_file.exists():
#             st.error(f"Theme CSS file not found: {css_file}")
#             return ""

#         try:
#             with open(css_file, 'r', encoding='utf-8') as f:
#                 css_content = f.read()

#             # Strip @import for fonts (handled separately)
#             font_pattern = r'@import\s+url\([\'"]?(https://fonts\.googleapis\.com/[^\'")\s]+)[\'"]?\);?\s*'
#             css_content = re.sub(font_pattern, '', css_content)

#             # Strip @import for theme_base.css (already loaded)
#             css_content = re.sub(r'@import\s+url\([\'"]?theme_base\.css[\'"]?\);?\s*', '', css_content)

#             return css_content

#         except Exception as e:
#             st.error(f"Error loading theme CSS: {e}")
#             return ""

#     def _inject_fonts(self, theme_data):
#         """Inject Google Fonts by reading @import urls from the theme's CSS file."""
#         css_file = self.themes_dir / theme_data['css_file']
#         if css_file.exists():
#             try:
#                 with open(css_file, 'r', encoding='utf-8') as f:
#                     css_content = f.read()
#                 font_pattern = r'@import\s+url\([\'"]?(https://fonts\.googleapis\.com/[^\'")\s]+)[\'"]?\);?'
#                 for font_url in re.findall(font_pattern, css_content):
#                     st.markdown(f'<link href="{font_url}" rel="stylesheet">', unsafe_allow_html=True)
#             except Exception:
#                 pass


# # ==============================================================================
# # CONVENIENCE FUNCTIONS
# # ==============================================================================

# def quick_theme_setup(default_theme='ocean', themes_dir='themes', key_prefix='theme_switcher'):
#     """
#     One-line theme setup. Location and enable/disable controlled by secrets.

#     Args:
#         default_theme: Theme to use by default
#         themes_dir: Directory containing theme CSS files
#         key_prefix: Unique prefix for widget keys

#     Returns:
#         ThemeSwitcher instance
#     """
#     return apply_theme(
#         default_theme=default_theme,
#         themes_dir=themes_dir,
#         show_selector=True,
#         allow_customization=False,
#         key_prefix=key_prefix
#     )


# def apply_theme(default_theme='rose_gold', themes_dir='themes',
#                 show_selector=True, allow_customization=False,
#                 selector_location=None, key_prefix='theme_switcher'):
#     """
#     Function-based API for applying themes.

#     selector_location is read from st.secrets['theme_ui_location'] if not
#     passed explicitly. Pass a value to override the secret.

#     Args:
#         default_theme: Default theme to use
#         themes_dir: Directory containing theme CSS files
#         show_selector: Whether to show theme selector
#         allow_customization: Whether to enable theme customization controls
#         selector_location: Override location ('sidebar', 'header', 'footer').
#                            If None, reads from secrets.
#         key_prefix: Unique prefix for this theme switcher instance

#     Returns:
#         ThemeSwitcher instance
#     """
#     ts_key = f'_ts_instance_{key_prefix}'
#     selector_rendered_key = f'_ts_selector_rendered_{key_prefix}'

#     # Always recreate the ThemeSwitcher so _discover_themes picks up
#     # any new/changed CSS files on every run.
#     # Only the selected theme key is persisted in session_state.
#     ts = ThemeSwitcher(
#         default_theme=default_theme,
#         themes_dir=themes_dir,
#         key_prefix=key_prefix
#     )
#     if ts_key not in st.session_state:
#         st.session_state[selector_rendered_key] = False
#     st.session_state[ts_key] = ts

#     if show_selector:
#         ts.render_selector(location=selector_location)
#         if not st.session_state[selector_rendered_key]:
#             st.session_state[selector_rendered_key] = True

#     ts.apply_theme()

#     if allow_customization:
#         _add_customization_controls(ts, selector_location or ts._get_ui_location())

#     return ts


# # ==============================================================================
# # CUSTOMIZATION (unchanged from original)
# # ==============================================================================

# def _add_customization_controls(ts, location='sidebar'):
#     """Add theme customization controls (font size, spacing, radius, accent color)."""
#     container = st.sidebar if location == 'sidebar' else st

#     if 'theme_customizations' not in st.session_state:
#         st.session_state.theme_customizations = {
#             'font_size_multiplier': 1.0,
#             'spacing_multiplier': 1.0,
#             'border_radius_multiplier': 1.0,
#             'custom_accent_color': None
#         }

#     with container:
#         st.markdown("---")
#         st.markdown("### ⚙️ Customize Theme")

#         font_size = st.slider("Font Size", 0.8, 1.3,
#             st.session_state.theme_customizations['font_size_multiplier'],
#             step=0.1, key="custom_font_size")
#         st.session_state.theme_customizations['font_size_multiplier'] = font_size

#         spacing = st.slider("Spacing", 0.7, 1.3,
#             st.session_state.theme_customizations['spacing_multiplier'],
#             step=0.1, key="custom_spacing")
#         st.session_state.theme_customizations['spacing_multiplier'] = spacing

#         radius = st.slider("Roundness", 0.0, 2.0,
#             st.session_state.theme_customizations['border_radius_multiplier'],
#             step=0.1, key="custom_radius")
#         st.session_state.theme_customizations['border_radius_multiplier'] = radius

#         use_custom_accent = st.checkbox("Custom Accent Color",
#             value=st.session_state.theme_customizations['custom_accent_color'] is not None,
#             key="use_custom_accent")

#         if use_custom_accent:
#             accent_color = st.color_picker("Pick Accent Color",
#                 value=st.session_state.theme_customizations['custom_accent_color'] or "#d4af37",
#                 key="custom_accent_color_picker")
#             st.session_state.theme_customizations['custom_accent_color'] = accent_color
#         else:
#             st.session_state.theme_customizations['custom_accent_color'] = None

#         if st.button("Reset Customizations", key="reset_custom"):
#             st.session_state.theme_customizations = {
#                 'font_size_multiplier': 1.0,
#                 'spacing_multiplier': 1.0,
#                 'border_radius_multiplier': 1.0,
#                 'custom_accent_color': None
#             }
#             st.rerun()

#     _apply_customization_css()


# def _apply_customization_css():
#     """Apply CSS customizations based on user settings."""
#     custom = st.session_state.theme_customizations

#     customization_css = f"""
# <style>
# /* === THEME CUSTOMIZATIONS === */
# :root {{
#     --custom-font-multiplier: {custom['font_size_multiplier']};
#     --custom-spacing-multiplier: {custom['spacing_multiplier']};
#     --custom-radius-multiplier: {custom['border_radius_multiplier']};
# }}
# h1 {{ font-size: calc(3.5rem * var(--custom-font-multiplier)) !important; }}
# h2 {{ font-size: calc(2rem * var(--custom-font-multiplier)) !important; }}
# h3 {{ font-size: calc(1.3rem * var(--custom-font-multiplier)) !important; }}
# p, label, div {{ font-size: calc(1rem * var(--custom-font-multiplier)) !important; }}
# .stButton > button {{
#     padding: calc(12px * var(--custom-spacing-multiplier)) calc(32px * var(--custom-spacing-multiplier)) !important;
# }}
# .stTextInput > div > div > input,
# .stTextArea > div > div > textarea {{
#     padding: calc(12px * var(--custom-spacing-multiplier)) calc(16px * var(--custom-spacing-multiplier)) !important;
# }}
# [data-testid="metric-container"] {{
#     padding: calc(1.5rem * var(--custom-spacing-multiplier)) !important;
# }}
# .stButton > button {{ border-radius: calc(12px * var(--custom-radius-multiplier)) !important; }}
# .stTextInput > div > div > input,
# .stTextArea > div > div > textarea,
# .stSelectbox > div > div {{
#     border-radius: calc(8px * var(--custom-radius-multiplier)) !important;
# }}
# [data-testid="metric-container"] {{ border-radius: calc(16px * var(--custom-radius-multiplier)) !important; }}
# """

#     if custom['custom_accent_color']:
#         customization_css += f"""
# .stButton > button {{
#     background: {custom['custom_accent_color']} !important;
#     border-color: {custom['custom_accent_color']} !important;
# }}
# h2 {{ color: {custom['custom_accent_color']} !important; }}
# .stTabs [aria-selected="true"] {{
#     background: {custom['custom_accent_color']} !important;
# }}
# a {{ color: {custom['custom_accent_color']} !important; }}
# """

#     customization_css += "</style>"
#     st.markdown(customization_css, unsafe_allow_html=True)
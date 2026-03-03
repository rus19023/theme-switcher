# theme_switcher/css_inject.py
import streamlit as st

def inject_icon_button_css():
    """
    Styles ONLY theme icon grid buttons (not expander header).
    Requires the grid to be wrapped in <div class="ts-theme-grid"> ... </div>
    """
    st.markdown("""
<style>
/* Make the theme icon buttons perfect squares and center emoji */
.ts-theme-grid div[data-testid="stButton"] > button {
  width: 48px !important;
  height: 48px !important;
  min-height: 48px !important;
  padding: 0 !important;

  display: flex !important;
  align-items: center !important;
  justify-content: center !important;

  font-size: 1.35rem !important;
  line-height: 1 !important;

  background: var(--theme-bg-card, rgba(255,255,255,0.06)) !important;
  border: 1px solid var(--theme-border-color, rgba(255,255,255,0.18)) !important;
  border-radius: 12px !important;

  box-shadow: none !important;
  transform: none !important;
}

/* Hover */
.ts-theme-grid div[data-testid="stButton"] > button:hover {
  background: var(--theme-bg-secondary, rgba(255,255,255,0.12)) !important;
  border-color: var(--theme-color-primary, rgba(255,255,255,0.35)) !important;
}

/* Remove internal label spacing so emoji is truly centered */
.ts-theme-grid div[data-testid="stButton"] > button p,
.ts-theme-grid div[data-testid="stButton"] > button span {
  margin: 0 !important;
  padding: 0 !important;
  line-height: 1 !important;
}
</style>
""", unsafe_allow_html=True)

def inject_tooltip_css():
    st.markdown("""
<style>
div[data-testid="stTooltipContent"] {
  background: var(--theme-bg-secondary, rgba(0,0,0,0.85)) !important;
  color: var(--theme-text-primary, rgba(255,255,255,0.95)) !important;
  border: 1px solid var(--theme-border-color, rgba(255,255,255,0.18)) !important;
  border-radius: var(--theme-radius-md, 10px) !important;
  font-size: 0.85rem !important;
  line-height: 1.2 !important;
}
</style>
""", unsafe_allow_html=True)

def inject_combined_css(base_css: str, theme_css: str):
    st.markdown(f"""
<style>
*, *::before, *::after {{ box-sizing: border-box; }}
{base_css}
{theme_css}
</style>
""", unsafe_allow_html=True)

def inject_font_links(font_urls: list[str]):
    for url in font_urls:
        st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

def inject_sticky_bar_css(position: str):
    if position == "header":
        css_position = "top: 0; left: 0; right: 0;"
        padding_target = ".block-container { padding-top: 3.5rem !important; }"
        border_side = "bottom"
    else:
        css_position = "bottom: 0; left: 0; right: 0;"
        padding_target = ".block-container { padding-bottom: 3.5rem !important; }"
        border_side = "top"

    st.markdown(f"""
<style>
.theme-bar {{
  position: fixed;
  {css_position}
  z-index: 9998;
  background: var(--theme-bg-secondary, rgba(0,0,0,0.75));
  backdrop-filter: blur(8px);
  padding: 6px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  border-{border_side}: 1px solid var(--theme-border-color, rgba(255,255,255,0.12));
}}
.theme-bar span.bar-label {{
  font-size: 0.75rem;
  opacity: 0.7;
  margin-right: 6px;
  white-space: nowrap;
}}
{padding_target}
</style>
""", unsafe_allow_html=True)
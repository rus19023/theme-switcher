# customize.py

import streamlit as st

def add_customization_controls(location_container):
    """
    location_container is st (main area)
    """
    if "theme_customizations" not in st.session_state:
        st.session_state.theme_customizations = {
            "font_size_multiplier": 1.0,
            "spacing_multiplier": 1.0,
            "border_radius_multiplier": 1.0,
            "custom_accent_color": None,
        }

    with location_container:
        st.markdown("---")
        st.markdown("### ⚙️ Customize Theme")

        c = st.session_state.theme_customizations

        c["font_size_multiplier"] = st.slider(
            "Font Size", 0.8, 1.3, c["font_size_multiplier"], step=0.1, key="custom_font_size"
        )
        c["spacing_multiplier"] = st.slider(
            "Spacing", 0.7, 1.3, c["spacing_multiplier"], step=0.1, key="custom_spacing"
        )
        c["border_radius_multiplier"] = st.slider(
            "Roundness", 0.0, 2.0, c["border_radius_multiplier"], step=0.1, key="custom_radius"
        )

        use_custom_accent = st.checkbox(
            "Custom Accent Color",
            value=c["custom_accent_color"] is not None,
            key="use_custom_accent",
        )

        if use_custom_accent:
            c["custom_accent_color"] = st.color_picker(
                "Pick Accent Color",
                value=c["custom_accent_color"] or "#d4af37",
                key="custom_accent_color_picker",
            )
        else:
            c["custom_accent_color"] = None

        if st.button("Reset Customizations", key="reset_custom"):
            st.session_state.theme_customizations = {
                "font_size_multiplier": 1.0,
                "spacing_multiplier": 1.0,
                "border_radius_multiplier": 1.0,
                "custom_accent_color": None,
            }
            st.rerun()

    apply_customization_css()

def apply_customization_css():
    c = st.session_state.get("theme_customizations", None)
    if not c:
        return

    css = f"""
    <style>
    :root {{
        --custom-font-multiplier: {c["font_size_multiplier"]};
        --custom-spacing-multiplier: {c["spacing_multiplier"]};
        --custom-radius-multiplier: {c["border_radius_multiplier"]};
    }}

    /* Scope typography: DO NOT apply to all divs globally */
    .stApp :is(p, label) {{
        font-size: calc(1rem * var(--custom-font-multiplier)) !important;
    }}
    .stApp div[data-testid="stMarkdownContainer"] {{
        font-size: calc(1rem * var(--custom-font-multiplier)) !important;
    }}

    .stButton > button {{
        padding: calc(12px * var(--custom-spacing-multiplier)) calc(32px * var(--custom-spacing-multiplier)) !important;
        border-radius: calc(12px * var(--custom-radius-multiplier)) !important;
    }}

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        padding: calc(12px * var(--custom-spacing-multiplier)) calc(16px * var(--custom-spacing-multiplier)) !important;
        border-radius: calc(8px * var(--custom-radius-multiplier)) !important;
    }}

    .stSelectbox > div > div {{
        border-radius: calc(8px * var(--custom-radius-multiplier)) !important;
    }}

    [data-testid="metric-container"] {{
        padding: calc(1.5rem * var(--custom-spacing-multiplier)) !important;
        border-radius: calc(16px * var(--custom-radius-multiplier)) !important;
    }}
    """

    if c.get("custom_accent_color"):
        css += f"""
        .stButton > button {{
            background: {c["custom_accent_color"]} !important;
            border-color: {c["custom_accent_color"]} !important;
        }}
        h2 {{ color: {c["custom_accent_color"]} !important; }}
        .stTabs [aria-selected="true"] {{
            background: {c["custom_accent_color"]} !important;
        }}
        a {{ color: {c["custom_accent_color"]} !important; }}
        """

    css += "</style>"

    st.markdown(css, unsafe_allow_html=True)
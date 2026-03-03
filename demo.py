"""
demo.py

Demo App to Showcase the Modular Theme Switcher

This demonstrates how to use the modular theme system in any Streamlit app.
"""

import streamlit as st
from theme_switcher import quick_theme_setup, apply_theme
import os as os
from theme_switcher.ui.font_gallery import render_font_gallery

# Page config
st.set_page_config(
    page_title="Theme Demo v2",
    page_icon="🎨",
    layout="wide"
)

# Quick theme setup - this is all you need!
ts = apply_theme(default_theme="mexico", selector_location="sidebar")

# Now build your app normally
st.title("Demo App for Testing ThemeSwitcher")
st.markdown("### Choose a new theme and it changes quickly!")


# Sample content
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Users", "12.5K", "+15%")

with col2:
    st.metric("Revenue", "$89.2K", "+23%")

with col3:
    st.metric("Growth Rate", "156%", "+45%")

with col4:
    st.metric("Satisfaction", "4.8/5", "+0.2")

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([ "Font Gallery", "Overview", "Settings", "Documentation"])

with tab1:
    render_font_gallery()

with tab2:
    st.markdown("## Welcome!")
    st.markdown("""
        This demo shows how easy it is to add professional themes to any Streamlit app.
        The theme system is completely modular - just drop the files into your project!
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Quick Setup")
        st.code("""
        from theme_switcher import quick_theme_setup

        # Add this at the start of your app
        quick_theme_setup()

        # That's it! Your app now has themes
                """, language="python")
    
    with col2:
        st.markdown("### Available Themes")
        # get list of themes from list of css files in themes folder, strip ".css"
        THEMES_DIR = os.path.join(os.path.dirname(__file__), "themes")
        THEMES = [f.replace(".css", "") for f in os.listdir(THEMES_DIR) if f.endswith(".css")] if os.path.exists(THEMES_DIR) else ["default"]
        for theme_key, theme_data in ts.available_themes.items():
            st.markdown(f"**{theme_data['name']}** - {theme_data['description']}")

with tab3:
    st.markdown("## Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Username", placeholder="Enter your username")
        st.text_input("Email", placeholder="your@email.com")
        st.text_input("API Key", type="password")
    
    with col2:
        st.selectbox("Region", ["US East", "US West", "EU Central", "Asia Pacific"])
        st.selectbox("Plan", ["Free", "Pro", "Enterprise"])
        st.selectbox("Timezone", ["UTC", "EST", "PST", "GMT"])
    
    st.markdown("---")
    
    st.checkbox("Enable notifications")
    st.checkbox("Auto-save preferences")
    st.checkbox("Dark mode sync")
    
    st.button("Save Settings")

with tab4:
    st.markdown("## How It Works")
    
    st.markdown("""
    ### Installation
    
    1. Copy `theme_switcher.py` to your project
    2. Copy the `themes/` folder to your project
    3. Import and use in your app
    
    ### Basic Usage
    
    ```python
    from theme_switcher import quick_theme_setup
    
    # Initialize themes (one line!)
    quick_theme_setup()
    
    # Build your app
    st.title("My App")
    ```
    
    ### Advanced Usage
    
    ```python
    from theme_switcher import ThemeSwitcher
    
    # Create custom instance
    ts = ThemeSwitcher(default_theme='cyberpunk')
    
    # Custom sidebar
    ts.render_sidebar(
        title="Choose Your Style",
        show_description=True
    )
    
    # Apply theme
    ts.apply_theme()
    
    # Get theme info
    info = ts.get_theme_info()
    st.write(f"Using: {info['name']}")
    ```
    
    ### Adding New Themes
    
    1. Create a new CSS file in `themes/` (e.g., `mytheme.css`)
    2. Add theme definition to `ThemeSwitcher.THEMES` dict
    3. That's it!
    
    ### File Structure
    
    ```
    your_project/
    ├── app.py
    ├── theme_switcher.py
    └── themes/
        ├── glassmorphism.css
        ├── cyberpunk.css
        ├── brutalist.css
        ├── luxury.css
        ├── academic.css
        ├── terminal.css
        ├── retro.css
        ├── corporate.css
        ├── nature.css
        └── neon.css
    ```
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 2rem; opacity: 0.7;">
        <p>Modular Theme System for Streamlit</p>
        <p>Drop-in solution • 10 professional themes • Fully customizable</p>
    </div>
""", unsafe_allow_html=True)


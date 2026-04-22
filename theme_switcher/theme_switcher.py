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
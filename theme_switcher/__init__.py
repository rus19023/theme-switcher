"""
Theme Switcher for Streamlit
A modular theming system with dropdown selector and hybrid theme discovery.
"""

from .api import apply_theme, quick_theme_setup
from .switcher import ThemeSwitcher

__all__ = ["apply_theme", "quick_theme_setup", "ThemeSwitcher"]
__version__ = '2.3.0'

# theme_switcher/loader.py
from pathlib import Path
import re
import base64

# Matches Google Fonts @import lines
_FONT_IMPORT = r'@import\s+url\([\'"]?(https://fonts\.googleapis\.com/[^\'")\s]+)[\'"]?\);?\s*'

# Matches @theme-image-credit: ... in CSS comments
_CREDIT_RE = r'@theme-image-credit:\s*(.+)'


def _read_text(path: Path) -> str:
    """Read file as UTF-8 text."""
    return path.read_text(encoding="utf-8")


def _image_to_base64(path: Path) -> str:
    """Convert image file to base64 data URI."""
    suffix = path.suffix.lower()
    mime = {
        ".jpg":  "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png":  "image/png",
        ".webp": "image/webp",
    }.get(suffix, "image/jpeg")
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"


def load_base_css(base_css_file: Path) -> str:
    """Load theme_base.css. Returns empty string if missing."""
    if not base_css_file.exists():
        return ""
    try:
        return _read_text(base_css_file)
    except Exception:
        return ""


def load_theme_css(theme_css_file: Path, images_dir: Path | None = None) -> tuple[str, list[str], dict]:
    """
    Load a theme CSS file and return (css, font_urls, meta).

    - Strips Google Fonts @import lines (returned separately as font_urls)
    - Strips @import url('theme_base.css') line
    - Replaces __BG_IMAGE__ placeholder with base64 data URI if image found in images_dir
    - Parses @theme-image-credit from header comment into meta dict

    images_dir convention: image file must be named {theme_stem}_bg.jpg/png/webp
    e.g. themes/images/pacific_bg.jpg for themes/pacific.css

    meta keys:
        image_credit: str | None  (may contain HTML)
    """
    if not theme_css_file.exists():
        return "", [], {}

    css = _read_text(theme_css_file)

    # Extract Google Fonts URLs before stripping
    font_urls = re.findall(_FONT_IMPORT, css)

    # Strip font imports (injected separately as <link> tags)
    css = re.sub(_FONT_IMPORT, "", css)

    # Strip base import (loaded separately)
    css = re.sub(r'@import\s+url\([\'"]?theme_base\.css[\'"]?\);?\s*', "", css)

    # Parse image credit from header comment
    meta = {}
    credit_match = re.search(_CREDIT_RE, css)
    if credit_match:
        meta["image_credit"] = credit_match.group(1).strip()

    # Embed background image as base64 if placeholder present
    if images_dir and "__BG_IMAGE__" in css:
        stem = theme_css_file.stem  # e.g. "pacific"
        for ext in (".jpg", ".jpeg", ".png", ".webp"):
            img_path = images_dir / f"{stem}_bg{ext}"
            if img_path.exists():
                data_uri = _image_to_base64(img_path)
                css = css.replace("__BG_IMAGE__", data_uri)
                break

    return css, font_urls, meta
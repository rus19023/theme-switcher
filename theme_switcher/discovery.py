# discovery.py 

from pathlib import Path
import re

def read_css_header_metadata(css_file: Path) -> dict:
    """
    Looks for first /* ... */ block and reads:
      @theme-name:
      @theme-icon:
      @theme-description:
    """
    try:
        text = css_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {}

    head = text[:2048]
    m = re.search(r"/\*([\s\S]*?)\*/", head)
    if not m:
        return {}

    block = m.group(1)

    def grab(tag: str):
        mm = re.search(rf"@{tag}\s*:\s*(.+)", block, flags=re.IGNORECASE)
        return mm.group(1).strip() if mm else None

    return {
        "name": grab("theme-name"),
        "icon": grab("theme-icon"),
        "description": grab("theme-description"),
    }

def discover_themes(themes_dir: Path, secrets_meta: dict | None = None) -> dict:
    """
    Returns dict keyed by theme key (stem) with metadata.
    Priority: secrets > CSS header > filename fallback
    """
    secrets_meta = secrets_meta or {}
    available = {}

    if not themes_dir.exists():
        return available

    for css_file in sorted(themes_dir.glob("*.css")):
        if css_file.stem in ("theme_base", "theme_template"):
            continue

        stem = css_file.stem
        header = read_css_header_metadata(css_file)
        secret = secrets_meta.get(stem, {}) if isinstance(secrets_meta, dict) else {}

        name = (secret.get("name") if secret else None) or header.get("name") or stem.replace("_", " ").title()
        icon = (secret.get("icon") if secret else None) or header.get("icon") or "🎨"
        desc = (secret.get("description") if secret else None) or header.get("description") or ""

        available[stem] = {
            "name": name,
            "icon": icon,
            "description": desc,
            "source": "custom" if header or css_file else "custom",
            "css_file": css_file.name,
        }

    return available
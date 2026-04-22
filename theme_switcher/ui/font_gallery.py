# ui/font_gallery.py

import streamlit as st
import streamlit.components.v1 as components
import requests
from urllib.parse import quote_plus
import math



def load_google_font_one(family: str, weights: str = "400;700"):
    family = (family or "").strip()
    if not family:
        return
    href = f"https://fonts.googleapis.com/css2?family={quote_plus(family)}:wght@{weights}&display=swap"
    st.markdown(f'<link href="{href}" rel="stylesheet">', unsafe_allow_html=True)


def _font_name(item):
    """Accept 'Inter' or {'name':'Inter'} or {'family':'Inter'}."""
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        for k in ("name", "family", "font", "title"):
            if k in item and isinstance(item[k], str):
                return item[k]
    return None

def load_google_fonts(fonts):
    """
    fonts can be:
      - list[str]
      - list[dict] with a 'name' (or 'family') field
      - dict[str, dict] keyed by font name
    """
    names = []

    if isinstance(fonts, dict):
        names = [k for k in fonts.keys() if isinstance(k, str)]
    else:
        for item in fonts:
            n = _font_name(item)
            if n:
                names.append(n)

    # remove duplicates
    seen = set()
    names = [n for n in names if not (n in seen or seen.add(n))]

    if not names:
        return

    family_parts = [
        f"family={quote_plus(n)}:wght@400;700"
        for n in names
    ]

    href = f"https://fonts.googleapis.com/css2?{'&'.join(family_parts)}&display=swap"

    st.markdown(f'<link href="{href}" rel="stylesheet">', unsafe_allow_html=True)







def get_google_fonts(api_key, sort="alpha"):
    """
    Fetch all Google Fonts

    sort options:
        alpha
        date
        popularity
        style
        trending
    """

    url = "https://www.googleapis.com/webfonts/v1/webfonts"

    params = {
        "key": api_key,
        "sort": sort
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Google Fonts API Error: {response.status_code} - {response.text}")

    data = response.json()

    fonts = [
        {
            "family": item["family"],
            "category": item["category"],
            "variants": item.get("variants", []),
            "subsets": item.get("subsets", []),
            "files": item.get("files", {}),
            "version": item.get("version")
        }
        for item in data["items"]
    ]

    return fonts

GOOGLE_FONTS = get_google_fonts(st.secrets['GOOGLE_FONT_API_KEY'])


def load_google_fonts_in_chunks(font_names, weights="400;700", chunk_size=8):
    """Load Google fonts with multiple <link> tags to avoid URL-length limits."""
    # de-dupe preserve order
    seen = set()
    names = [n for n in font_names if n and not (n in seen or seen.add(n))]

    for i in range(0, len(names), chunk_size):
        chunk = names[i:i + chunk_size]
        family_parts = [f"family={quote_plus(n)}:wght@{weights}" for n in chunk]
        href = f"https://fonts.googleapis.com/css2?{'&'.join(family_parts)}&display=swap"
        st.markdown(f'<link href="{href}" rel="stylesheet">', unsafe_allow_html=True)


def render_font_gallery():
    st.header("Google Font Gallery")

    # ---- Search ----
    q = st.text_input("Search fonts", "")

    # Normalize to list of dicts with 'family'
    normalized = []
    for item in GOOGLE_FONTS:
        if isinstance(item, str):
            normalized.append({"family": item})
        elif isinstance(item, dict):
            fam = item.get("family") or item.get("name")
            if isinstance(fam, str) and fam.strip():
                normalized.append({**item, "family": fam.strip()})

    # Filter
    if q.strip():
        qq = q.strip().lower()
        normalized = [f for f in normalized if qq in f["family"].lower()]

    if not normalized:
        st.info("No fonts match your search.")
        return

    # ---- Pagination (48 per page) ----
    page_size = 48
    total = len(normalized)
    total_pages = max(1, math.ceil(total / page_size))

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)
    with col2:
        st.caption(f"{total} fonts")
    with col3:
        st.caption("Tip: Search to narrow results, then page through 48 at a time.")

    start = (page - 1) * page_size
    end = min(start + page_size, total)
    page_fonts = normalized[start:end]

    # ---- Load only fonts for this page (reliable + fast) ----
    font_names = [f["family"] for f in page_fonts]
    load_google_fonts_in_chunks(font_names, chunk_size=8)  # 48 fonts => 6 requests

    # ---- Render cards ----
    cols_per_row = 4  # 48 => 12 rows of 4
    rows = [page_fonts[i:i+cols_per_row] for i in range(0, len(page_fonts), cols_per_row)]

    for row in rows:
        cols = st.columns(cols_per_row)
        for i in range(cols_per_row):
            with cols[i]:
                if i >= len(row):
                    st.empty()
                    continue

                font = row[i]["family"]
                category = row[i].get("category", "")

                st.markdown(
                    f"""
                    <div style="
                        border:1px solid rgba(255,255,255,0.15);
                        border-radius:12px;
                        padding:14px;
                        background: rgba(255,255,255,0.04);
                        margin-bottom:12px;
                    ">
                      <div style="display:flex; justify-content:space-between; gap:10px; margin-bottom:6px;">
                        <div style="font-size:0.9rem; opacity:0.85;">
                          {font}
                        </div>
                        <div style="font-size:0.75rem; opacity:0.6;">
                          {category}
                        </div>
                      </div>

                      <div style="font-family:'{font}', sans-serif; font-size:22px; line-height:1.2;">
                        The quick brown fox jumps over the lazy dog.
                      </div>

                      <div style="margin-top:10px; font-size:0.8rem; opacity:0.7;">
                        CSS: <code>font-family: '{font}', sans-serif;</code>
                      </div>

                      <div style="margin-top:6px; font-size:0.8rem; opacity:0.7;">
                        Import: <code>@import url('https://fonts.googleapis.com/css2?family={quote_plus(font)}:wght@400;700&display=swap');</code>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
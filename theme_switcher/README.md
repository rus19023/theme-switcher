# 🎨 Streamlit Modular Theme System

A drop-in theme system for Streamlit apps with many professional themes included, plus support for custom themes. No configuration needed — just import and use!

## 🚀 Quick Start

```python
from theme_switcher import quick_theme_setup

# Add this one line at the start of your app
quick_theme_setup()

# Build your app normally
st.title("My Themed App")
st.write("Theme switching is automatic!")
```

That's it! Your app now has a theme selector in the sidebar.

## 📦 Installation

1. **Copy files to your project:**
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

2. **Run your app:**
   ```bash
   streamlit run app.py
   ```


---


---

## 💡 Usage Examples

### Basic Usage
```python
from theme_switcher import quick_theme_setup

quick_theme_setup()

st.title("My App")
```

### Advanced Usage
```python
from theme_switcher import ThemeSwitcher

ts = ThemeSwitcher(default_theme='retro')

ts.render_sidebar(
    title="🎨 Choose Your Style",
    show_description=True
)

ts.apply_theme()

info = ts.get_theme_info()
st.write(f"Current theme: {info['name']}")
```

### Set Default Theme
```python
from theme_switcher import quick_theme_setup

quick_theme_setup(default_theme='retro')
```

---

## 🎨 Creating Custom Themes

### 1. Create CSS File

Create a new file in the `themes/` folder (e.g., `themes/myTheme.css`):

```css
/* My Custom Theme */
:root {
    --primary: #ff6b6b;
    --secondary: #4ecdc4;
}

.stApp {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    font-family: 'Your Font', sans-serif;
    color: white;
}

h1 {
    font-size: 3rem !important;
    color: var(--primary) !important;
}

.stButton > button {
    background: var(--primary) !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
}
```

### 2. Register Theme

Add your theme's css file to the themes folder.

Your theme will appear in the sidebar automatically.

---

## 🛠️ Customization

### Hide Streamlit Branding

All themes automatically hide the main menu, footer, header, and deploy button.

### Theme Persistence

Themes are stored in `st.session_state` and persist for the duration of the session. To add cross-session persistence, modify `theme_switcher.py` to use a database or server-side storage.

### Sidebar Customization

```python
ts.render_sidebar(
    title="Pick a Vibe",
    show_description=False
)
```

---

## 🎯 Use Cases

- **White-label apps** - Let clients choose their brand colors
- **User preferences** - Give users control over appearance
- **Context switching** - Different themes for dev/staging/prod
- **Accessibility** - Offer high-contrast or dyslexia-friendly options
- **Branding** - Match your company's style guide

---

## 📝 Component Styling

Each theme styles these Streamlit components:
- Headers (h1, h2, h3)
- Buttons
- Text inputs
- Text areas
- Select boxes and multiselects
- Checkboxes and radio buttons
- Alerts and info messages
- Expanders
- Metrics
- Tabs
- Sliders
- Dividers (hr)
- Scrollbars

---

## 🐛 Troubleshooting

**Themes not appearing**
- Make sure the `themes/` folder is in the same directory as `theme_switcher.py`.
- Check that CSS files have the correct names and are saved as UTF-8.
- Verify Google Fonts are loading (check browser console).

**Theme not applying**
- Ensure `apply_theme()` is called after `render_sidebar()`.
- Check for CSS conflicts with any custom CSS in your app.
- Try `st.rerun()` after changing themes.

**Info icon not showing**
- The info icon uses a CSS `::before` pseudo-element. If your Streamlit version uses a different alert `data-testid`, update the selector in `tis.css` accordingly.

**Cyberpunk theme performance**
- The cyberpunk theme includes animations. If you experience performance issues, disable them by commenting out the `@keyframes` blocks in `cyberpunk.css`.

---

## 📄 License

Feel free to use, modify, and distribute. No attribution required.

## 🤝 Contributing

Want to add a theme?
1. Create the CSS file in `themes/`.
2. Add it to the `THEMES` dict in `theme_switcher.py`.
3. Submit a PR or share it with the community!

---

**Pro tip:** Mix and match CSS variables from different themes to create your own unique style!
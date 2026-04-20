# AGENTS.md

This file provides guidance to agentic coding agents operating in this repository.

## Project Overview

This is a simple static website for GitHub Pages deployment. The project consists of vanilla HTML, CSS, and JavaScript with no build tools, frameworks, or test suites.

## Build/Lint/Test Commands

This is a static site — no build commands required. To preview locally:

```bash
# Simple local server
python3 -m http.server 8000

# Or using Node.js (if npx available)
npx serve .
```

### Deployment

The site deploys automatically via GitHub Actions when pushing to `main`:

```bash
# Manual deploy trigger (via GitHub UI)
gh workflow run pages.yml
```

### GitHub Pages Setup

If GitHub Pages is not enabled:
1. Go to repository **Settings → Pages**
2. Under **Build and deployment**, select **GitHub Actions** as source
3. Next push to `main` triggers deployment

## Code Style Guidelines

### General

- Use semantic HTML5 elements (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`)
- Keep JavaScript vanilla — no frameworks unless explicitly requested
- Use meaningful class names that describe content, not appearance

### HTML

```html
<!-- DO: Semantic structure -->
<header><nav><main><footer>

<!-- DON'T: Non-semantic divs -->
<div class="header"><div class="main">
```

- Include meta tags: charset, viewport, description
- Link CSS in `<head>`, JS before `</body>`

### CSS

```css
/* DO: CSS custom properties for theming */
:root { --color-accent: #0066cc; }

/* DO: Box-sizing reset */
* { box-sizing: border-box; margin: 0; padding: 0; }

/* DO: Responsive breakpoints */
@media (min-width: 640px) { ... }
```

- Use CSS variables for colors/spacing
- Use `rem` for font sizes
- Mobile-first responsive design

### JavaScript

```javascript
// DO: DOMContentLoaded wrapper
document.addEventListener('DOMContentLoaded', () => { ... });

// DON'T: Inline handlers
<button onclick="handleClick()">

// DO: const for values that don't change
const init = () => { ... };
```

- No semicolons required but recommended
- Use ES6+ syntax (const, let, arrow functions)
- Keep functions small and focused

### File Structure

```
/
├── index.html      # Main HTML document
├── styles.css      # All styles
├── main.js         # All JavaScript
├── .github/
│   └── workflows/
│       └── pages.yml  # GitHub Actions deploy workflow
└── README.md
```

### Git Workflow

- Branch name: `main`
- Commit changes, push to origin
- GitHub Actions auto-deploys on push to `main`
- Do not commit built artifacts or cache files

### Error Handling

- JS: Use try/catch for potentially failing operations
- HTML: Validate links point to existing resources
- CSS: Check for cascade conflicts

### Performance

- Minimize external dependencies
- Lazy load images with `loading="lazy"`
- Use CSS animations over JS where possible

## VS Code Configuration

Project includes `.vscode/settings.json` with basic settings. No additional extensions required for this project.

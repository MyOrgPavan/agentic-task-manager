# Plan: Add Footer with Copyright to base.html

## Scope
Frontend — Jinja2 template (`base.html`) and custom CSS (`style.css`).

## Ticket / Issue
Issue #26 — Add a footer with copyright to base.html

## Risk Level
Low. Isolated UI change; no backend logic, no routes, no data model modifications. All child templates inherit from `base.html` and will automatically pick up the footer. The CSS change is additive (no existing styles are removed).

## Description
Add a sticky footer to the bottom of every page displaying:  
`© 2026 Task Manager. All rights reserved.`

The footer must stick to the bottom of the viewport when content is shorter than the screen (sticky footer via flexbox), and naturally follow content when the page scrolls.

Two files need changes:
1. **`backend/templates/base.html`** — wrap the main content area in a `<main>` tag and insert a `<footer>` tag with the copyright text.
2. **`backend/static/style.css`** — add flexbox rules to make the footer sticky (`body { display: flex; flex-direction: column; min-height: 100vh; }` and `main { flex: 1; }`).

## Success Criteria (checklist)
- [ ] Footer text `© 2026 Task Manager. All rights reserved.` appears on every page.
- [ ] Footer is visually separated from the content (Bootstrap utility padding / border-top).
- [ ] Footer sticks to the bottom of the viewport when page content is short.
- [ ] Footer scrolls down naturally when page content exceeds viewport height.
- [ ] No regressions in layout of existing pages (navbar, flash messages, content blocks).
- [ ] All child templates render correctly (no broken `{% block %}` or `{% extends %}` references).

## Files to Modify (specific paths)
1. `backend/templates/base.html`
2. `backend/static/style.css`

## Implementation Steps (numbered)

### Step 1 — Edit `backend/templates/base.html`
1. Wrap the existing content `<div class="container">` (including flash messages and `{% block content %}`) inside a `<main>` element with Bootstrap class `flex-shrink-0` to integrate with the sticky footer flexbox layout.
2. Before the closing `</body>`, add a `<footer>` element with:
   - Bootstrap classes: `bg-dark text-white text-center py-3 mt-auto`
   - Content: `© 2026 Task Manager. All rights reserved.`
3. The `mt-auto` class pushes the footer to the bottom within the flexbox column.

### Step 2 — Edit `backend/static/style.css`
1. Add CSS rules for sticky footer:
   ```css
   body {
       display: flex;
       flex-direction: column;
       min-height: 100vh;
   }
   main {
       flex: 1;
   }
   ```
2. The `body` rule establishes a flex column that spans the full viewport height.
3. The `main` rule makes the content area expand to fill available space, pushing the footer down.

## Rollback Strategy
1. **If the footer layout breaks pages** (e.g., content overlaps or is misaligned):
   - Remove the `<main>` wrapper and `<footer>` element from `base.html` — restore the original structure.
   - Remove the flexbox CSS rules from `style.css` — restore the original single-line rule.
2. All changes are confined to two files with no dependencies; a clean `git checkout backend/templates/base.html backend/static/style.css` fully reverts.
3. No database migrations, no environment variable changes, no package dependency changes — full rollback in under one minute.

# Plan: Add Footer with Copyright to base.html

## Scope
Frontend — HTML template change only.

## Ticket / Issue
#19 — Add a footer with copyright to base.html

## Risk Level
Low — HTML template change only, no logic changes.

## Description
Add a `<footer>` element to `base.html` that displays the project name ("Agentic Task Manager"), the copyright year (2026), and a link to the GitHub repository. The footer should be styled with Bootstrap 5 utility classes and stick to the bottom of the page.

## Success Criteria
- [ ] Footer is present on all pages (since it is in `base.html`)
- [ ] Footer contains project name and copyright
- [ ] Footer is styled consistently with Bootstrap 5
- [ ] Footer sticks to the bottom of the page

## Files to Modify
- `backend/templates/base.html` — add the footer HTML
- `backend/static/style.css` — add sticky footer CSS

## Implementation Steps

1. **Open `backend/templates/base.html`** and locate the closing `</body>` tag.
2. **Add a `<footer>` element** before `</body>` (after the Bootstrap JS script), containing:
   - A `<div class="container">` wrapper to align with the rest of the layout.
   - A `<p class="text-center text-muted mb-0 py-3">` (or similar Bootstrap utility classes) with the text: `© 2026 Agentic Task Manager`.
   - A link to the GitHub repo: `<a href="..." target="_blank" rel="noopener noreferrer">GitHub</a>`.
3. **Open `backend/static/style.css`** and add CSS to ensure the footer sticks to the bottom:
   - Set `<html>` and `<body>` to `height: 100%`.
   - Use a flexbox approach: `body { display: flex; flex-direction: column; }`, the main content area gets `flex: 1`, and the footer sits naturally at the bottom.
   - Since there is no dedicated wrapper div around the main content, either:
     - Wrap the nav + container in a `<main>` or `<div class="content">` block, **or**
     - Use `margin-top: auto` on the `<footer>` to push it down (simpler and avoids restructuring the template).
   - **Recommended approach** (minimal template change): Add `margin-top: auto` to the footer via CSS. The body gets `display: flex; flex-direction: column; min-height: 100vh;` to ensure full viewport height.
4. **Verify the footer** appears on every page by checking several templates that extend `base.html` (e.g., `index.html`, `login.html`, `projects.html`).
5. **Review styling** — confirm footer text, link color, and alignment are consistent with the Bootstrap 5 theme (e.g., muted text, centered, no awkward gaps).

## Rollback Strategy

If the footer causes layout issues (e.g., content no longer fills the page correctly, or the footer overlaps content):

1. **Revert `backend/static/style.css`** — remove the flexbox / sticky footer styles added in step 3.
2. **Revert `backend/templates/base.html`** — remove the `<footer>` element added in step 2.
3. If using version control, run:
   ```bash
   git checkout backend/templates/base.html backend/static/style.css
   ```

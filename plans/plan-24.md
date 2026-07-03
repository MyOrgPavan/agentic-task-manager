# Plan: Add Footer to base.html

## Scope
Frontend — Jinja2 template (`base.html`) and CSS (`style.css`). No backend logic, no database changes, no new routes.

## Ticket / Issue
Issue #24 — Add a footer with copyright to base.html. The footer must be sticky and display "© 2026 Task Manager. All rights reserved."

## Risk Level
Low. Isolated UI change; no logic, models, or API surface area affected. Visual regression is the only risk.

## Description
`base.html` currently ends abruptly after the Bootstrap JS script tag with no footer element. A `<footer>` element containing the copyright line needs to be added inside the `<body>` (after the main content container). The CSS must be updated to implement a sticky footer pattern (flexbox on `<body>`, `flex: 1` on the content wrapper) so the footer stays at the bottom even on pages with little content.

## Success Criteria (checklist)
- [ ] Footer appears on every page that extends `base.html`
- [ ] Footer text reads exactly: "© 2026 Task Manager. All rights reserved."
- [ ] Footer is sticky (always at the bottom of the viewport when content is short)
- [ ] Footer does not overlap or interfere with page content
- [ ] Existing tests still pass
- [ ] Visual appearance is consistent with Bootstrap 5 styling (muted text, centered, padded)

## Files to Modify
1. `backend/templates/base.html` — Add `<footer>` element after the closing `</div>` of the `.container` (or after the flash messages block)
2. `backend/static/style.css` — Add sticky footer CSS rules (`body` flexbox, `main`/`.wrapper` flex-grow)

## Implementation Steps
1. In `backend/templates/base.html`, wrap the existing `<nav>` and `<div class="container">` in a `<main>` (or a `<div class="content-wrapper">`) so the sticky footer pattern has a flex child to grow.
2. Add a `<footer class="footer mt-auto py-3 bg-light">` element after the closing `</main>` tag (or wrapper), before `</body>`.
3. Inside the footer, add a `<div class="container">` with the copyright text `© 2026 Task Manager. All rights reserved.` using Bootstrap's `text-muted text-center` classes.
4. In `backend/static/style.css`, add:
   - `html, body { height: 100%; }`
   - `body { display: flex; flex-direction: column; }`
   - `.content-wrapper { flex: 1 0 auto; }` (or equivalent selector for the wrapper/main element)
   - Ensure the footer uses `flex-shrink: 0` (Bootstrap's `mt-auto` handles this when body is a flex column).

## Rollback Strategy
- **Revert commit:** `git revert <commit-hash>` and push.
- **Manual rollback:** Restore `base.html` and `style.css` from the commit before this change via `git checkout <prior-hash> -- backend/templates/base.html backend/static/style.css`.
- Verify rollback by loading any page and confirming the footer is gone.

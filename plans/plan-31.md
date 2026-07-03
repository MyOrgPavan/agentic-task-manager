# Plan: Modify Footer Copyright Text in base.html

## Scope
Frontend — Jinja2 template (`base.html`) only.

## Ticket / Issue
Issue #31 — Modify footer with copyright to base.html

## Risk Level
Low. Single text change in one file; no backend logic, no routes, no data model modifications, no structural changes to the layout.

## Description
Update the existing footer text in `base.html` from:
`© 2026 Task Manager. All rights reserved.`
to:
`© 2026 Task Manager. All rights reserved. test123`

The sticky footer layout (flexbox in `style.css`, `mt-auto` on `<footer>`) is already implemented and requires no changes.

## Success Criteria (checklist)
- [ ] Footer reads `© 2026 Task Manager. All rights reserved. test123` on every page.
- [ ] Footer retains its sticky behavior at the bottom of the viewport (no regression).
- [ ] No regressions in layout (navbar, flash messages, content blocks).
- [ ] All child templates continue to render correctly.

## Files to Modify (specific paths)
1. `backend/templates/base.html` — update the copyright text inside the existing `<footer>` element.

## Implementation Steps (numbered)
1. Open `backend/templates/base.html`.
2. Locate the `<footer>` element containing `&copy; 2026 Task Manager. All rights reserved.`
3. Append ` test123` to the existing text node, resulting in `&copy; 2026 Task Manager. All rights reserved. test123`
4. Verify appearance by loading any page (e.g., home page, login page) and confirming the updated text displays at the bottom.

## Rollback Strategy
1. Revert the single-line text change: restore the original `&copy; 2026 Task Manager. All rights reserved.` string in the `<footer>`.
2. `git checkout backend/templates/base.html` fully reverts the change.
3. No database migrations, environment variables, or package changes — full rollback in under one minute.

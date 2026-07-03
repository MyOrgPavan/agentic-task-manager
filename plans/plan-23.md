## Scope
frontend

## Ticket / Issue
#23

## Risk Level
low

## Description
Add a dark mode toggle button to the navbar that switches between light and dark themes using CSS custom properties. The preference is stored in localStorage so it persists across page loads.

## Success Criteria
- [ ] A sun/moon toggle icon appears in the navbar
- [ ] Clicking the toggle switches between light and dark themes
- [ ] Preference persists across page reloads (localStorage)
- [ ] All existing pages work correctly in both themes
- [ ] No visual glitches on form inputs, alerts, or buttons

## Files to Modify
- `backend/templates/base.html` — add toggle button in navbar, add dark mode CSS variables, add toggle JavaScript
- `backend/static/style.css` — add dark mode CSS overrides

## Implementation Steps
1. Add a dark mode toggle button (sun/moon icon) to the right side of the navbar in base.html
2. Add CSS custom properties for light and dark themes in base.html `<style>` block
3. Add JavaScript toggle logic that switches `data-bs-theme` on `<html>` and saves preference to localStorage
4. Add dark mode overrides in style.css (background, cards, forms, alerts)

## Rollback Strategy
Revert changes to `backend/templates/base.html` and `backend/static/style.css`

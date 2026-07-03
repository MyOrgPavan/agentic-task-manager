---
type: Component
title: Static Assets
description: CSS stylesheets supporting the Bootstrap-based frontend.
resource: /home/pavan/Workspace/Projects/Github sdlc/agentic-task-manager/backend/static/
tags: [components, frontend, css, static]
timestamp: "2026-07-03T09:45:00Z"
---

# Static Assets

## Files

| File | Purpose |
|------|---------|
| `style.css` | Custom styles, sticky footer layout |

## style.css Highlights

- `.container` max-width 960px
- Sticky footer: `body { display: flex; flex-direction: column; min-height: 100vh; }` + `main { flex: 1; }`

## Conventions

- Minimal custom CSS — prefer Bootstrap 5 utility classes
- CSS custom properties for theme colors
- Responsive design via Bootstrap grid

## See Also

- [/components/frontend-templates](/components/frontend-templates.md)
- [/agents/frontend](/agents/frontend.md)

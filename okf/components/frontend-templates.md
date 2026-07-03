---
type: Component
title: Frontend Templates
description: Jinja2 HTML templates using Bootstrap 5 for the task management UI.
resource: /home/pavan/Workspace/Projects/Github sdlc/agentic-task-manager/backend/templates/
tags: [components, frontend, templates, jinja2, bootstrap]
timestamp: "2026-07-03T09:45:00Z"
---

# Frontend Templates

## Template Hierarchy

```
base.html                  ← Layout: nav, flash messages, footer, blocks
├── index.html             ← Landing page
├── auth/
│   ├── login.html         ← Login form
│   └── register.html      ← Registration form
├── projects/
│   ├── list.html          ← Project listing
│   ├── detail.html        ← Single project with tasks
│   └── form.html          ← Create/edit project
├── tasks/
│   ├── detail.html        ← Single task with comments
│   └── form.html          ← Create/edit task
```

## base.html Blocks

| Block | Purpose |
|-------|---------|
| `title` | Page title |
| `content` | Main content area |
| `scripts` | Extra JS per page |

## Footer (Added via PR #23)

Sticky footer with copyright, always at bottom via CSS:
```css
body { display: flex; flex-direction: column; min-height: 100vh; }
main { flex: 1; }
```

## Conventions

- All templates extend `base.html`
- Bootstrap 5 classes for layout and components
- Flash messages use dismissable alert component
- Navigation items adapt to `current_user.is_authenticated`
- Forms rendered with `form.hidden_tag()` and Bootstrap form classes

## See Also

- [/components/static-assets](/components/static-assets.md)
- [/components/flask-app](/components/flask-app.md)
- [/agents/frontend](/agents/frontend.md)

# 07 — Local Development

How to run the Flask web app locally with Docker or Python.

## Prerequisites

- Docker and Docker Compose (for containerized setup)
- Python 3.11+ (for direct setup)
- Git

---

## Docker Setup (Recommended)

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd agentic-task-manager
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your secrets
```

### 3. Start Services

```bash
docker-compose up
```

### 4. Access Application

Open http://localhost:5000

### 5. Stop Services

```bash
docker-compose down
```

---

## Python Setup (Direct)

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd agentic-task-manager
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your secrets
```

### 5. Run Application

```bash
flask run
# or
python -m flask run
```

### 6. Access Application

Open http://localhost:5000

---

## Running Tests

```bash
# With Docker
docker-compose exec web pytest backend/tests/ -v

# Without Docker
source venv/bin/activate
pytest backend/tests/ -v
```

### Test Coverage

29 tests covering:
- User registration and login
- Project CRUD operations
- Task CRUD operations
- Comment CRUD operations
- Input validation
- Authentication requirements

---

## Code Quality

### Linting

```bash
ruff check backend/ scripts/ mcp-servers/
```

### Type Checking

```bash
mypy backend/ scripts/ mcp-servers/ --ignore-missing-imports
```

### Auto-fix Lint Issues

```bash
ruff check --fix backend/
```

---

## Database

### Development (SQLite)

- Automatic: SQLite database created on first run
- Location: `instance/app.db`
- No configuration needed

### Production (PostgreSQL)

1. Update `.env`:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/agentic_task_manager
   ```

2. Start PostgreSQL:
   ```bash
   docker run -d --name postgres \
     -e POSTGRES_USER=user \
     -e POSTGRES_PASSWORD=password \
     -e POSTGRES_DB=agentic_task_manager \
     -p 5432:5432 \
     postgres:15
   ```

---

## Project Structure

```
agentic-task-manager/
├── backend/
│   ├── app.py              # Flask app factory
│   ├── models.py           # SQLAlchemy models
│   ├── routes/             # Blueprint modules
│   ├── templates/          # Jinja2 HTML templates
│   ├── static/             # CSS/JS
│   └── tests/              # pytest tests
├── mcp-servers/            # MCP tool servers
├── scripts/                # Helper scripts
├── .github/                # Workflows and configs
├── Dockerfile              # Container setup
├── docker-compose.yml      # Local development
├── requirements.txt        # Python dependencies
└── pyproject.toml          # Project config
```

---

## IDE Configuration

### VS Code

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.typeCheckingMode": "strict"
}
```

### PyCharm

1. Set Python interpreter to `venv/bin/python`
2. Enable Ruff in Settings > Tools > External Tools
3. Configure mypy in Settings > Tools > Python Integrated Tools

---

## Common Development Tasks

### Add New Route

1. Create route in `backend/routes/<module>.py`
2. Register blueprint in `backend/app.py`
3. Add template in `backend/templates/`
4. Add tests in `backend/tests/test_api.py`

### Add New Model

1. Define model in `backend/models.py`
2. Run `db.create_all()` (auto in app startup)
3. Add tests in `backend/tests/test_models.py`

### Add New Workflow

1. Create `.github/workflows/<name>.yml`
2. Add traceability comment: `# <requirement-id>`
3. Add to workflow list in `DEMONSTRATION.md`
# Plan 17: Health-Check Endpoint

## Scope
Backend only — new Flask blueprint for a `GET /api/health` endpoint returning JSON with service status, database connectivity, and uptime. Includes unit/integration tests.

## Ticket / Issue
#17

## Risk Level
Low — new endpoint only; no existing code modified. No authentication, no data mutation, no new dependencies.

## Description
Add `GET /api/health` that returns a JSON response with three fields:

```json
{
  "status": "ok",
  "db": "connected",
  "uptime": 1234.56
}
```

- `status`: always `"ok"` on success.
- `db`: `"connected"` if a trivial DB query succeeds, `"disconnected"` otherwise (catch `SQLAlchemy`/operational errors so the endpoint never 5xxes).
- `uptime`: seconds since the Flask app was created (store a `start_time` in `app.config` or as a module-level timestamp on first import).

The endpoint must respond in < 100 ms (trivially met — no expensive operations).

## Success Criteria (checklist)

- [ ] `GET /api/health` returns 200 with JSON body containing `status`, `db`, `uptime` keys.
- [ ] When database is reachable, `db` field is `"connected"`.
- [ ] When database is unreachable (simulated in test), endpoint still returns 200 and `db` field is `"disconnected"`.
- [ ] `uptime` is a positive float increasing over time.
- [ ] Existing tests still pass (`pytest backend/tests/ -v`).
- [ ] Ruff lint passes (`ruff check backend/`).
- [ ] MyPy type-check passes (`mypy backend/`).
- [ ] Response time < 100 ms (verified by manual timing or a quick `time` curl).

## Files to Modify (specific paths)

| Action | Path |
|--------|------|
| **Create** | `backend/routes/health.py` — new health blueprint |
| **Modify** | `backend/app.py` — register `health_bp` in `create_app()`; store `start_time` |
| **Create** | `backend/tests/test_health.py` — tests for the health endpoint |

## Implementation Steps (numbered)

1. **Create `backend/routes/health.py`**
   - Define `health_bp = Blueprint("health", __name__)`.
   - Import `db` from `backend.models`.
   - On import, record `start_time = time.time()` as a module-level constant.
   - Implement `@health_bp.route("/api/health")` with method `GET`.
   - Inside:
     - Compute `uptime = time.time() - start_time`.
     - Attempt a lightweight DB query (e.g. `db.session.execute(text("SELECT 1"))`) and catch any `SQLAlchemy` exception.
     - If query succeeds, set `db_status = "connected"`; otherwise `db_status = "disconnected"`.
     - Return `jsonify({"status": "ok", "db": db_status, "uptime": round(uptime, 2)})`.
   - Import `text` from `sqlalchemy` (already available via SQLAlchemy dependency).

2. **Modify `backend/app.py`**
   - Import `health_bp` from `backend.routes.health`.
   - Register it in `create_app()`: `app.register_blueprint(health_bp)`.
   - Optionally store `app.config["START_TIME"] = time.time()` if a more official pattern is preferred over module-level variable (the module-level approach is simpler and equally correct).

3. **Create `backend/tests/test_health.py`**
   - Use the same `app` and `client` fixtures from pytest-flask (or replicate the fixture pattern from `test_api.py` — no `conftest.py` exists, so mirror the inline app fixture).
   - **Test `test_health_success`**: issue `client.get("/api/health")`, assert 200, assert JSON keys (`status`, `db`, `uptime`), assert `status == "ok"`, assert `db == "connected"`, assert `uptime > 0`.
   - **Test `test_health_db_disconnected`**: monkey-patch or temporarily break the DB (e.g. set `app.config["SQLALCHEMY_DATABASE_URI"]` to an invalid URI and re-init, or use `unittest.mock.patch` on `db.session.execute` to raise an exception). Assert 200, `status == "ok"`, `db == "disconnected"`.
   - **Test `test_health_uptime_increases`**: call endpoint twice with a small `time.sleep(0.01)` between; assert second uptime > first uptime.

4. **Verify**
   - Run `ruff check backend/` — no new issues.
   - Run `mypy backend/` — no new type errors.
   - Run `pytest backend/tests/ -v` — all tests pass (existing + new).
   - Manually start the app (`flask run` or `gunicorn`), `curl localhost:5000/api/health`, confirm JSON and timing.

## Rollback Strategy

1. Revert `backend/app.py` (remove import and registration of `health_bp`).
2. Delete `backend/routes/health.py`.
3. Delete `backend/tests/test_health.py`.
4. Run `pytest backend/tests/ -v` to confirm no regressions.

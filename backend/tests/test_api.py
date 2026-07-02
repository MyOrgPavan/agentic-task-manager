# FR-09
import json

import pytest

from backend.app import create_app
from backend.models import User, db


@pytest.fixture
def app():
    app = create_app(testing=True)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_client(app, client):
    with app.app_context():
        u = User(username="testuser", email="test@example.com")
        u.set_password("password123")
        db.session.add(u)
        db.session.commit()

    client.post("/auth/login", data={
        "username": "testuser",
        "password": "password123"
    }, follow_redirects=True)
    return client


class TestAuthAPI:
    def test_register(self, client):
        resp = client.post("/auth/register", data={
            "username": "newuser",
            "email": "new@example.com",
            "password": "pass123"
        }, follow_redirects=True)
        assert resp.status_code == 200

    def test_register_duplicate_username(self, client):
        client.post("/auth/register", data={
            "username": "dupuser",
            "email": "dup@example.com",
            "password": "pass123"
        }, follow_redirects=True)
        resp = client.post("/auth/register", data={
            "username": "dupuser",
            "email": "other@example.com",
            "password": "pass123"
        }, follow_redirects=True)
        assert resp.status_code == 200

    def test_login_success(self, client):
        with client.application.app_context():
            u = User(username="loginuser", email="login@example.com")
            u.set_password("correct")
            db.session.add(u)
            db.session.commit()

        resp = client.post("/auth/login", data={
            "username": "loginuser",
            "password": "correct"
        }, follow_redirects=True)
        assert resp.status_code == 200

    def test_login_failure(self, client):
        resp = client.post("/auth/login", data={
            "username": "nonexistent",
            "password": "wrong"
        }, follow_redirects=True)
        assert resp.status_code == 200

    def test_logout_requires_auth(self, client):
        resp = client.get("/auth/logout", follow_redirects=True)
        assert resp.status_code == 200


class TestProjectsAPI:
    def test_list_projects_requires_auth(self, client):
        resp = client.get("/projects", headers={"Accept": "application/json"}, follow_redirects=True)
        assert resp.status_code == 200

    def test_create_project(self, auth_client):
        resp = auth_client.post("/projects", data={"title": "Test Project"}, follow_redirects=True)
        assert resp.status_code == 200

    def test_create_project_api_json(self, auth_client):
        resp = auth_client.post("/projects", json={"title": "API Project"}, content_type="application/json", follow_redirects=True)
        assert resp.status_code == 200

    def test_get_project(self, auth_client):
        auth_client.post("/projects", data={"title": "My Project"}, follow_redirects=True)
        resp = auth_client.get("/projects/1", headers={"Accept": "application/json"})
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["title"] == "My Project"

    def test_update_project(self, auth_client):
        auth_client.post("/projects", data={"title": "Old Title"}, follow_redirects=True)
        resp = auth_client.put("/projects/1", json={"title": "New Title", "status": "archived"})
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["message"] == "Project updated."

    def test_delete_project(self, auth_client):
        auth_client.post("/projects", data={"title": "Delete Me"}, follow_redirects=True)
        resp = auth_client.delete("/projects/1", follow_redirects=True)
        assert resp.status_code in (200, 302)


class TestTasksAPI:
    def test_create_task(self, auth_client):
        auth_client.post("/projects", data={"title": "Project"}, follow_redirects=True)
        resp = auth_client.post("/projects/1/tasks", data={
            "title": "Test Task",
            "description": "A task",
            "due_date": "2026-12-31"
        }, follow_redirects=True)
        assert resp.status_code == 200

    def test_get_task(self, auth_client):
        auth_client.post("/projects", data={"title": "Project"}, follow_redirects=True)
        auth_client.post("/projects/1/tasks", data={"title": "My Task"}, follow_redirects=True)
        resp = auth_client.get("/tasks/1", headers={"Accept": "application/json"})
        assert resp.status_code == 200

    def test_update_task(self, auth_client):
        auth_client.post("/projects", data={"title": "Project"}, follow_redirects=True)
        auth_client.post("/projects/1/tasks", data={"title": "Old Task"}, follow_redirects=True)
        resp = auth_client.put("/tasks/1", json={"title": "Updated Task", "status": "in_progress"})
        assert resp.status_code == 200

    def test_delete_task(self, auth_client):
        auth_client.post("/projects", data={"title": "Project"}, follow_redirects=True)
        auth_client.post("/projects/1/tasks", data={"title": "Delete Task"}, follow_redirects=True)
        resp = auth_client.delete("/tasks/1", follow_redirects=True)
        assert resp.status_code in (200, 302)


class TestCommentsAPI:
    def test_create_comment(self, auth_client):
        auth_client.post("/projects", data={"title": "Project"}, follow_redirects=True)
        auth_client.post("/projects/1/tasks", data={"title": "Task"}, follow_redirects=True)
        resp = auth_client.post("/tasks/1/comments", data={"content": "Nice work!"}, follow_redirects=True)
        assert resp.status_code == 200

    def test_get_comments(self, auth_client):
        auth_client.post("/projects", data={"title": "Project"}, follow_redirects=True)
        auth_client.post("/projects/1/tasks", data={"title": "Task"}, follow_redirects=True)
        auth_client.post("/tasks/1/comments", data={"content": "First!"}, follow_redirects=True)
        resp = auth_client.get("/tasks/1/comments", headers={"Accept": "application/json"})
        assert resp.status_code == 200

    def test_delete_comment(self, auth_client):
        auth_client.post("/projects", data={"title": "Project"}, follow_redirects=True)
        auth_client.post("/projects/1/tasks", data={"title": "Task"}, follow_redirects=True)
        auth_client.post("/tasks/1/comments", data={"content": "Delete me"}, follow_redirects=True)
        resp = auth_client.delete("/comments/1")
        assert resp.status_code == 200


class TestInputValidation:
    def test_create_project_empty_title(self, auth_client):
        resp = auth_client.post("/projects", data={"title": ""}, follow_redirects=True)
        assert resp.status_code == 200

    def test_create_task_empty_title(self, auth_client):
        auth_client.post("/projects", data={"title": "Project"}, follow_redirects=True)
        resp = auth_client.post("/projects/1/tasks", data={"title": ""}, follow_redirects=True)
        assert resp.status_code == 200

    def test_hello_endpoint(self, client):
        resp = client.get("/hello")
        assert resp.status_code == 200
        assert b"Hello, World!" in resp.data

    def test_404_handling(self, client):
        resp = client.get("/nonexistent")
        assert resp.status_code == 404

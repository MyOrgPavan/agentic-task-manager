# FR-09
import pytest

from backend.app import create_app
from backend.models import Comment, Project, Task, User, db


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
def _user(app):
    with app.app_context():
        u = User(username="testuser", email="test@example.com")
        u.set_password("password123")
        db.session.add(u)
        db.session.commit()
        return u


class TestUserModel:
    def test_create_user(self, app):
        with app.app_context():
            u = User(username="alice", email="alice@example.com")
            u.set_password("secret")
            db.session.add(u)
            db.session.commit()
            assert u.id is not None
            assert u.password_hash != "secret"
            assert u.check_password("secret") is True
            assert u.check_password("wrong") is False

    def test_unique_username(self, app):
        with app.app_context():
            u1 = User(username="uniqueuser", email="u1@example.com")
            u1.set_password("pass")
            db.session.add(u1)
            db.session.commit()
            u2 = User(username="uniqueuser", email="u2@example.com")
            u2.set_password("pass")
            db.session.add(u2)
            with pytest.raises(Exception):
                db.session.commit()


class TestProjectModel:
    def test_create_project(self, app):
        with app.app_context():
            u = User(username="projuser", email="proj@example.com")
            u.set_password("pass")
            db.session.add(u)
            db.session.commit()
            p = Project(title="Test Project", description="A test", user_id=u.id)
            db.session.add(p)
            db.session.commit()
            assert p.id is not None
            assert p.status == "active"
            assert p.priority == "medium"

    def test_project_owner_relationship(self, app):
        with app.app_context():
            u = User(username="owneruser", email="owner@example.com")
            u.set_password("pass")
            db.session.add(u)
            db.session.commit()
            p = Project(title="My Project", user_id=u.id)
            db.session.add(p)
            db.session.commit()
            project = db.session.get(Project, p.id)
            assert project.owner.username == "owneruser"


class TestTaskModel:
    def test_create_task(self, app):
        with app.app_context():
            u = User(username="taskuser", email="task@example.com")
            u.set_password("pass")
            db.session.add(u)
            db.session.commit()
            p = Project(title="Project", user_id=u.id)
            db.session.add(p)
            db.session.commit()
            t = Task(title="Test Task", project_id=p.id)
            db.session.add(t)
            db.session.commit()
            assert t.id is not None
            assert t.status == "todo"

    def test_task_project_relationship(self, app):
        with app.app_context():
            u = User(username="reluser", email="rel@example.com")
            u.set_password("pass")
            db.session.add(u)
            db.session.commit()
            p = Project(title="Project", user_id=u.id)
            db.session.add(p)
            db.session.commit()
            t = Task(title="Task", project_id=p.id)
            db.session.add(t)
            db.session.commit()
            task = db.session.get(Task, t.id)
            assert task.project.title == "Project"
            assert task.project.tasks.count() == 1


class TestCommentModel:
    def test_create_comment(self, app):
        with app.app_context():
            u = User(username="commentuser", email="comment@example.com")
            u.set_password("pass")
            db.session.add(u)
            db.session.commit()
            p = Project(title="Project", user_id=u.id)
            db.session.add(p)
            db.session.commit()
            t = Task(title="Task", project_id=p.id)
            db.session.add(t)
            db.session.commit()
            c = Comment(content="A comment", user_id=u.id, task_id=t.id)
            db.session.add(c)
            db.session.commit()
            assert c.id is not None
            comment = db.session.get(Comment, c.id)
            assert comment.author.username == "commentuser"

    def test_comment_task_relationship(self, app):
        with app.app_context():
            u = User(username="relcomment", email="relc@example.com")
            u.set_password("pass")
            db.session.add(u)
            db.session.commit()
            p = Project(title="Project", user_id=u.id)
            db.session.add(p)
            db.session.commit()
            t = Task(title="Task", project_id=p.id)
            db.session.add(t)
            db.session.commit()
            c = Comment(content="Comment", user_id=u.id, task_id=t.id)
            db.session.add(c)
            db.session.commit()
            task = db.session.get(Task, t.id)
            assert task.comments.count() == 1
            assert task.comments.first().content == "Comment"

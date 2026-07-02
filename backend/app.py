# FR-01, FR-02, FR-03, FR-04, FR-05, FR-06, FR-07, FR-08
import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_login import LoginManager
from backend.models import db, User

load_dotenv()

login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def create_app(testing=False):
    app = Flask(__name__, template_folder="templates", static_folder="static")

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///app.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["WTF_CSRF_ENABLED"] = False

    if testing:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    db.init_app(app)
    login_manager.init_app(app)

    from backend.routes.auth import auth_bp
    from backend.routes.projects import projects_bp
    from backend.routes.tasks import tasks_bp
    from backend.routes.comments import comments_bp
    from backend.routes.hello import hello_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(projects_bp, url_prefix="/projects")
    app.register_blueprint(tasks_bp, url_prefix="")
    app.register_blueprint(comments_bp, url_prefix="")
    app.register_blueprint(hello_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.errorhandler(404)
    def not_found(e):
        return {"error": "Not found"}, 404

    @app.errorhandler(500)
    def server_error(e):
        return {"error": "Internal server error"}, 500

    with app.app_context():
        db.create_all()

    return app

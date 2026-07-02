from flask import Blueprint, render_template

hello_bp = Blueprint("hello", __name__, template_folder="../templates")


@hello_bp.route("/hello")
def hello() -> str:
    return render_template("hello.html")

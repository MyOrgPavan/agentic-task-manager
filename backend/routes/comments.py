# FR-05, FR-06
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from backend.models import db, Project, Task, Comment

comments_bp = Blueprint("comments", __name__, template_folder="../templates")


@comments_bp.route("/tasks/<int:task_id>/comments", methods=["GET"])
@login_required
def list_comments(task_id):
    task = Task.query.join(Project).filter(Task.id == task_id, Project.user_id == current_user.id).first_or_404()
    comments = Comment.query.filter_by(task_id=task.id).order_by(Comment.created_at.asc()).all()
    if request.headers.get("Accept") == "application/json":
        return jsonify([{
            "id": c.id, "content": c.content, "author": c.author.username,
            "created_at": c.created_at.isoformat()
        } for c in comments])
    return render_template("task_detail.html", task=task, comments=comments)


@comments_bp.route("/tasks/<int:task_id>/comments", methods=["POST"])
@login_required
def create_comment(task_id):
    task = Task.query.join(Project).filter(Task.id == task_id, Project.user_id == current_user.id).first_or_404()
    content = request.form.get("content", "").strip()
    if not content:
        flash("Comment cannot be empty.", "danger")
        return redirect(url_for("tasks.get_task", task_id=task.id))

    comment = Comment(content=content, user_id=current_user.id, task_id=task.id)
    db.session.add(comment)
    db.session.commit()
    flash("Comment added.", "success")
    return redirect(url_for("tasks.get_task", task_id=task.id))


@comments_bp.route("/comments/<int:comment_id>", methods=["DELETE"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id, user_id=current_user.id).first_or_404()
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted."})

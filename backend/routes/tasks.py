# FR-04, FR-06
from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from backend.models import Project, Task, db

tasks_bp = Blueprint("tasks", __name__, template_folder="../templates")


@tasks_bp.route("/projects/<int:project_id>/tasks", methods=["GET"])
@login_required
def list_tasks(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()
    tasks = Task.query.filter_by(project_id=project.id).order_by(Task.created_at.desc()).all()
    if request.headers.get("Accept") == "application/json":
        return jsonify([{
            "id": t.id, "title": t.title, "status": t.status,
            "assignee": t.assignee.username if t.assignee else None,
            "due_date": t.due_date.isoformat() if t.due_date else None
        } for t in tasks])
    return render_template("project_detail.html", project=project, tasks=tasks)


@tasks_bp.route("/projects/<int:project_id>/tasks", methods=["POST"])
@login_required
def create_task(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    due_date_str = request.form.get("due_date", "").strip()

    if not title:
        flash("Title is required.", "danger")
        return redirect(url_for("projects.get_project", project_id=project.id))

    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format.", "danger")
            return redirect(url_for("projects.get_project", project_id=project.id))

    task = Task(title=title, description=description, due_date=due_date, project_id=project.id)
    db.session.add(task)
    db.session.commit()
    flash("Task created.", "success")
    return redirect(url_for("projects.get_project", project_id=project.id))


@tasks_bp.route("/tasks/<int:task_id>", methods=["GET"])
@login_required
def get_task(task_id):
    task = Task.query.join(Project).filter(Task.id == task_id, Project.user_id == current_user.id).first_or_404()
    if request.headers.get("Accept") == "application/json":
        return jsonify({
            "id": task.id, "title": task.title, "description": task.description,
            "status": task.status, "due_date": task.due_date.isoformat() if task.due_date else None,
            "project_id": task.project_id
        })
    return render_template("task_detail.html", task=task)


@tasks_bp.route("/tasks/<int:task_id>", methods=["PUT"])
@login_required
def update_task(task_id):
    task = Task.query.join(Project).filter(Task.id == task_id, Project.user_id == current_user.id).first_or_404()
    data = request.get_json()
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.status = data.get("status", task.status)
    if "due_date" in data and data["due_date"]:
        task.due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
    db.session.commit()
    return jsonify({"message": "Task updated."})


@tasks_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id):
    task = Task.query.join(Project).filter(Task.id == task_id, Project.user_id == current_user.id).first_or_404()
    project_id = task.project_id
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.", "info")
    return redirect(url_for("projects.get_project", project_id=project_id))

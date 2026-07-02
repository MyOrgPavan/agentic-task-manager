# FR-03, FR-06
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from backend.models import db, Project

projects_bp = Blueprint("projects", __name__, template_folder="../templates")


@projects_bp.route("", methods=["GET"])
@login_required
def list_projects():
    projects = Project.query.filter_by(user_id=current_user.id).order_by(Project.updated_at.desc()).all()
    if request.headers.get("Accept") == "application/json":
        return jsonify([{
            "id": p.id, "title": p.title, "description": p.description,
            "status": p.status, "priority": p.priority, "created_at": p.created_at.isoformat()
        } for p in projects])
    return render_template("projects.html", projects=projects)


@projects_bp.route("", methods=["POST"])
@login_required
def create_project():
    if request.headers.get("Content-Type") == "application/json":
        data = request.get_json()
        title = data.get("title", "").strip()
        description = data.get("description", "").strip()
        priority = data.get("priority", "medium")
    else:
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "medium")

    if not title:
        flash("Title is required.", "danger")
        return redirect(url_for("projects.list_projects"))

    project = Project(title=title, description=description, priority=priority, user_id=current_user.id)
    db.session.add(project)
    db.session.commit()
    flash("Project created.", "success")
    return redirect(url_for("projects.list_projects"))


@projects_bp.route("/<int:project_id>", methods=["GET"])
@login_required
def get_project(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()
    if request.headers.get("Accept") == "application/json":
        return jsonify({
            "id": project.id, "title": project.title, "description": project.description,
            "status": project.status, "priority": project.priority,
            "tasks": [{
                "id": t.id, "title": t.title, "status": t.status,
                "assignee": t.assignee.username if t.assignee else None,
                "due_date": t.due_date.isoformat() if t.due_date else None
            } for t in project.tasks.all()]
        })
    return render_template("project_detail.html", project=project)


@projects_bp.route("/<int:project_id>", methods=["PUT"])
@login_required
def update_project(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()
    data = request.get_json()
    project.title = data.get("title", project.title)
    project.description = data.get("description", project.description)
    project.status = data.get("status", project.status)
    project.priority = data.get("priority", project.priority)
    db.session.commit()
    return jsonify({"message": "Project updated."})


@projects_bp.route("/<int:project_id>", methods=["DELETE"])
@login_required
def delete_project(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()
    db.session.delete(project)
    db.session.commit()
    if request.headers.get("Accept") == "application/json":
        return jsonify({"message": "Project deleted."})
    flash("Project deleted.", "info")
    return redirect(url_for("projects.list_projects"))

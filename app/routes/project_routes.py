from flask import Blueprint, render_template, request, redirect
from ..extensions import db
from ..models.project import Project

project_bp = Blueprint("project", __name__)

@project_bp.route("/project/add", methods=["GET", "POST"])
def add_project():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        project = Project(title=title, description=description)
        db.session.add(project)
        db.session.commit()

        return redirect("/")

    return render_template("project/add_project.html")
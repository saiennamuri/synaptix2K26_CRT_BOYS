from flask import Blueprint, render_template, request, redirect
from ..extensions import db
from ..models.skill import Skill

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/add_skill", methods=["GET", "POST"])
def add_skill():
    if request.method == "POST":
        skill_name = request.form["skill_name"]

        if not Skill.query.filter_by(skill_name=skill_name).first():
            skill = Skill(skill_name=skill_name)
            db.session.add(skill)
            db.session.commit()

        return redirect("/admin/add_skill")

    return render_template("admin/add_skill.html")
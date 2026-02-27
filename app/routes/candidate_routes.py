from flask import Blueprint, render_template, request, redirect
from ..extensions import db
from ..models.candidate import Candidate

candidate_bp = Blueprint("candidate", __name__)

@candidate_bp.route("/")
def home():
    return render_template("index.html")

@candidate_bp.route("/candidate/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        candidate = Candidate(full_name=name, email=email)
        db.session.add(candidate)
        db.session.commit()

        return redirect("/")

    return render_template("candidate/register.html")
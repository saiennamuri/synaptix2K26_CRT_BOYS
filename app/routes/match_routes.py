from flask import Blueprint, render_template
from ..services.matching_engine import run_matching
from ..models.match import Match
from ..extensions import db

match_bp = Blueprint("match", __name__)

@match_bp.route("/match/<int:candidate_id>/<int:project_id>")
def match(candidate_id, project_id):

    score, explanation = run_matching(candidate_id, project_id)

    match = Match(candidate_id=candidate_id, project_id=project_id, match_score=score)
    db.session.add(match)
    db.session.commit()

    return render_template("match/results.html", score=score, explanation=explanation)
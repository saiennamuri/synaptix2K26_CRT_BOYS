from app.models.candidate import CandidateSkill
from app.models.project import ProjectSkill
from .scoring_service import calculate_score
from .explanation_service import generate_explanation

def run_matching(candidate_id, project_id):

    candidate_skills = CandidateSkill.query.filter_by(candidate_id=candidate_id).all()
    project_skills = ProjectSkill.query.filter_by(project_id=project_id).all()

    score = calculate_score(candidate_skills, project_skills)
    explanation = generate_explanation(candidate_skills, project_skills)

    return score, explanation
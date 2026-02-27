from ..extensions import db

class Candidate(db.Model):
    __tablename__ = "candidates"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    education = db.Column(db.String(100))
    experience_years = db.Column(db.Float, default=0)

    skills = db.relationship("CandidateSkill", backref="candidate", cascade="all, delete")


class CandidateSkill(db.Model):
    __tablename__ = "candidate_skills"

    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidates.id"))
    skill_id = db.Column(db.Integer, db.ForeignKey("skills.id"))
    proficiency_level = db.Column(db.Integer)
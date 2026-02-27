from ..extensions import db

class Match(db.Model):
    __tablename__ = "matches"

    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer)
    project_id = db.Column(db.Integer)
    match_score = db.Column(db.Float)
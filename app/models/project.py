from ..extensions import db

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)

    required_skills = db.relationship("ProjectSkill", backref="project", cascade="all, delete")


class ProjectSkill(db.Model):
    __tablename__ = "project_skills"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    skill_id = db.Column(db.Integer, db.ForeignKey("skills.id"))
    weight = db.Column(db.Integer, nullable=False)
    minimum_proficiency = db.Column(db.Integer, default=1)
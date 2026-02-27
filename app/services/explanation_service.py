from app.models.skill import Skill

def generate_explanation(candidate_skills, project_skills):

    explanation = []

    for ps in project_skills:
        skill = Skill.query.get(ps.skill_id)
        matched = False

        for cs in candidate_skills:
            if ps.skill_id == cs.skill_id:
                matched = True
                if cs.proficiency_level >= ps.minimum_proficiency:
                    explanation.append(f"✔ {skill.skill_name} matched")
                else:
                    explanation.append(f"⚠ {skill.skill_name} below required level")

        if not matched:
            explanation.append(f"❌ {skill.skill_name} missing")

    return explanation
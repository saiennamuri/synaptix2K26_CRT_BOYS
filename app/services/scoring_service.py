def calculate_score(candidate_skills, project_skills):

    total_weight = sum(ps.weight for ps in project_skills)
    matched_weight = 0

    for ps in project_skills:
        for cs in candidate_skills:
            if ps.skill_id == cs.skill_id:
                if cs.proficiency_level >= ps.minimum_proficiency:
                    matched_weight += ps.weight

    if total_weight == 0:
        return 0

    return round((matched_weight / total_weight) * 100, 2)
def calculate_overall_score(skill_scores):
    """
    Calculate the simple average
    of all skill scores.
    """

    if not skill_scores:

        return 0

    total = sum(
        skill_scores.values()
    )

    number_of_skills = len(
        skill_scores
    )

    return round(
        total / number_of_skills
    )


def calculate_weighted_score(
    skill_scores,
    weights
):
    """
    Calculate job-specific
    weighted competency score.
    """

    total_score = 0
    total_weight = 0

    for skill, weight in weights.items():

        candidate_score = skill_scores.get(
            skill,
            0
        )

        total_score += (
            candidate_score * weight
        )

        total_weight += weight

    if total_weight == 0:

        return 0

    return round(
        total_score / total_weight
    )


def get_readiness_level(score):

    if score >= 80:

        return "JOB READY 🟢"

    elif score >= 65:

        return "ALMOST READY 🟡"

    elif score >= 50:

        return "DEVELOPING 🟠"

    else:

        return "NEEDS UPSKILLING 🔴"


def show_score(score):

    print("\n" + "=" * 50)
    print("             CAREER READINESS")
    print("=" * 50)

    print(
        f"\nCareer Readiness Score: {score}%"
    )

    print(
        f"Status: {get_readiness_level(score)}"
    )

    print("=" * 50)


# TESTING

if __name__ == "__main__":

    skill_scores = {

        "Python": 100,
        "SQL": 100,
        "DSA": 50,
        "Backend": 100,
        "System Design": 0

    }

    backend_weights = {

        "Python": 0.20,
        "SQL": 0.15,
        "DSA": 0.20,
        "Backend": 0.25,
        "System Design": 0.20

    }

    score = calculate_weighted_score(
        skill_scores,
        backend_weights
    )

    show_score(score)
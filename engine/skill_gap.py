def calculate_skill_gaps(
    skill_scores,
    job_requirements
):

    gaps = {}

    for skill, required_score in job_requirements.items():

        candidate_score = skill_scores.get(
            skill,
            0
        )

        gap = required_score - candidate_score

        gaps[skill] = {

            "required": required_score,

            "current": candidate_score,

            "gap": max(gap, 0)

        }

    return gaps


def classify_gap(gap):

    if gap == 0:

        return "Strong 🟢"

    elif gap <= 10:

        return "Minor Gap 🟡"

    elif gap <= 25:

        return "Moderate Gap 🟠"

    else:

        return "Critical Gap 🔴"


def show_skill_gaps(gaps):

    print("\n" + "=" * 65)
    print("                 SKILL GAP ANALYSIS")
    print("=" * 65)

    if not gaps:

        print("\nNo skill requirements found.")

        return

    print(
        f"\n{'Skill':<20}"
        f"{'Required':<12}"
        f"{'Current':<12}"
        f"{'Gap':<10}"
        f"Status"
    )

    print("-" * 65)

    for skill, data in gaps.items():

        status = classify_gap(
            data["gap"]
        )

        print(
            f"{skill:<20}"
            f"{data['required']:<12}"
            f"{data['current']:<12}"
            f"{data['gap']:<10}"
            f"{status}"
        )

    print("=" * 65)


# TESTING

if __name__ == "__main__":

    skill_scores = {

        "Python": 100,
        "SQL": 100,
        "DSA": 50,
        "Backend": 100,
        "System Design": 0

    }

    backend_requirements = {

        "Python": 70,
        "SQL": 75,
        "DSA": 65,
        "Backend": 75,
        "System Design": 60

    }

    gaps = calculate_skill_gaps(
        skill_scores,
        backend_requirements
    )

    show_skill_gaps(gaps)
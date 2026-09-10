import json


def load_courses():

    with open("data/courses.json", "r") as file:
        return json.load(file)


def recommend_courses(skill_gaps):

    courses = load_courses()

    recommendations = []

    for skill, gap_data in skill_gaps.items():

        gap = gap_data["gap"]

        # No gap means no course is required
        if gap == 0:
            continue

        matching_courses = []

        for course in courses:

            if course["skill"] == skill:

                matching_courses.append(
                    course
                )

        # Beginner courses first
        matching_courses.sort(
            key=lambda course:
            0
            if course["level"] == "Beginner"
            else 1
        )

        recommendations.append({

            "skill": skill,

            "gap": gap,

            "courses": matching_courses

        })

    # Biggest gap first
    recommendations.sort(
        key=lambda item: item["gap"],
        reverse=True
    )

    return recommendations


def show_learning_path(
    recommendations
):

    print("\n" + "=" * 70)
    print("             PERSONALIZED LEARNING PATH")
    print("=" * 70)

    if not recommendations:

        print(
            "\n🎉 No major skill gaps found!"
        )

        print(
            "You are ready for your target role."
        )

        return

    step = 1

    for recommendation in recommendations:

        skill = recommendation["skill"]

        gap = recommendation["gap"]

        courses = recommendation["courses"]

        print(f"\n🔴 {skill}")

        print(
            f"   Skill Gap: {gap} points"
        )

        if not courses:

            print(
                "   ⚠ No course available for this skill."
            )

            continue

        for course in courses:

            print(
                f"\n   STEP {step}"
            )

            print(
                f"   📘 {course['name']}"
            )

            print(
                f"   Level: {course['level']}"
            )

            print(
                f"   Duration: {course['duration']}"
            )

            print(
                f"   Type: {course['type']}"
            )

            step += 1

    print("\n" + "=" * 70)


# TESTING

if __name__ == "__main__":

    skill_gaps = {

        "Python": {

            "required": 70,
            "current": 100,
            "gap": 0

        },

        "SQL": {

            "required": 75,
            "current": 100,
            "gap": 0

        },

        "DSA": {

            "required": 65,
            "current": 50,
            "gap": 15

        },

        "Backend": {

            "required": 75,
            "current": 100,
            "gap": 0

        },

        "System Design": {

            "required": 60,
            "current": 0,
            "gap": 60

        }

    }

    recommendations = recommend_courses(
        skill_gaps
    )

    show_learning_path(
        recommendations
    )
import json


def load_courses():

    with open("data/courses.json", "r") as file:

        return json.load(file)


def recommend_courses(skill_gaps):

    courses = load_courses()

    recommendations = []

    for skill, gap_data in skill_gaps.items():

        gap = gap_data["gap"]

        if gap == 0:
            continue

        matching_courses = []

        for course in courses:

            if course["skill"] == skill:

                matching_courses.append(course)

        matching_courses.sort(
            key=lambda course:
            0 if course["level"] == "Beginner" else 1
        )

        recommendations.append({

            "skill": skill,

            "gap": gap,

            "courses": matching_courses

        })

    recommendations.sort(
        key=lambda item: item["gap"],
        reverse=True
    )

    return recommendations


def show_learning_path(
    recommendations,
    learning_progress=None
):

    if learning_progress is None:

        learning_progress = {}

    print("\n" + "=" * 70)
    print("             PERSONALIZED LEARNING PATH")
    print("=" * 70)

    if not recommendations:

        print("\n🎉 No major skill gaps found!")

        print("You are ready for your target role.")

        return

    step = 1

    for recommendation in recommendations:

        skill = recommendation["skill"]

        gap = recommendation["gap"]

        courses = recommendation["courses"]

        print(f"\n🔴 {skill}")

        print(f"   Skill Gap: {gap} points")

        if not courses:

            print(
                "   ⚠ No course available for this skill."
            )

            continue

        for course in courses:

            course_name = course["name"]

            status = learning_progress.get(
                course_name,
                "Not Started"
            )

            print(f"\n   STEP {step}")

            print(f"   📘 {course_name}")

            print(
                f"   Level: {course['level']}"
            )

            print(
                f"   Duration: {course['duration']}"
            )

            print(
                f"   Type: {course['type']}"
            )

            print(
                f"   Status: {status}"
            )

            step += 1

    print("\n" + "=" * 70)


def update_course_status(
    learning_progress,
    course_name,
    status
):

    learning_progress[course_name] = status

    return learning_progress



def get_next_course(recommendations, learning_progress):
    for recommendation in recommendations:
        courses = recommendation["courses"]

        for course in courses:
            course_name = course["name"]
            status = learning_progress.get(course_name, "Not Started")

            if status == "Not Started":
                return course

    return None
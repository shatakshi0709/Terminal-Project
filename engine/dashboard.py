from engine.recommender import get_job_by_title
from engine.scoring import (
    calculate_weighted_score,
    get_readiness_level
)
from engine.skill_gap import calculate_skill_gaps
from engine.learning_path import (
    recommend_courses,
    get_next_course
)
from engine.certification import get_verified_skills


def show_dashboard(profile, skill_scores):

    print("\n")
    print("╔" + "═" * 58 + "╗")
    print(
        "║" +
        "SMART CAREER DASHBOARD".center(58) +
        "║"
    )
    print("╚" + "═" * 58 + "╝")

    if not profile:

        print("\n⚠ Please create a candidate profile first.")
        return

    if not skill_scores:

        print("\n⚠ Please take the competency diagnostic first.")
        return

    target_job = get_job_by_title(
        profile["target_role"]
    )

    if not target_job:

        print("\n⚠ Target job role not found.")
        return

    # --------------------------------------------------------
    # PROFILE
    # --------------------------------------------------------

    print("\n👤 CANDIDATE")
    print("-" * 60)

    print(
        f"  Name        : {profile['name']}"
    )

    print(
        f"  Education   : {profile['education']}"
    )

    print(
        f"  Experience  : {profile['experience']}"
    )

    print(
        f"  Target Role : {profile['target_role']}"
    )

    print(
        f"  Location    : {profile['location']}"
    )

    # --------------------------------------------------------
    # READINESS
    # --------------------------------------------------------

    readiness_score = calculate_weighted_score(
        skill_scores,
        target_job["weights"]
    )

    print("\n🎯 CAREER READINESS")
    print("-" * 60)

    print(
        f"  Readiness Score : {readiness_score}%"
    )

    print(
        f"  Status          : "
        f"{get_readiness_level(readiness_score)}"
    )

    # --------------------------------------------------------
    # SKILLS
    # --------------------------------------------------------

    print("\n📊 SKILL SCORES")
    print("-" * 60)

    for skill, score in skill_scores.items():

        print(
            f"  {skill:<20} {score}%"
        )

    # --------------------------------------------------------
    # SKILL GAPS
    # --------------------------------------------------------

    gaps = calculate_skill_gaps(
        skill_scores,
        target_job["requirements"]
    )

    print("\n🔍 SKILL GAPS")
    print("-" * 60)

    gap_found = False

    for skill, data in gaps.items():

        if data["gap"] > 0:

            gap_found = True

            print(
                f"  {skill:<20}"
                f"Gap: {data['gap']}"
            )

    if not gap_found:

        print("  🎉 No skill gaps found!")

    # --------------------------------------------------------
    # LEARNING
    # --------------------------------------------------------

    recommendations = recommend_courses(
        gaps
    )

    learning_progress = profile.get(
        "learning_progress",
        {}
    )

    next_course = get_next_course(
        recommendations,
        learning_progress
    )

    print("\n📚 LEARNING PROGRESS")
    print("-" * 60)

    completed = 0
    total = 0

    for course_name, status in learning_progress.items():

        total += 1

        if status == "Completed":
            completed += 1

    print(
        f"  Courses Tracked   : {total}"
    )

    print(
        f"  Courses Completed : {completed}"
    )

    if next_course:

        print(
            f"\n  🎯 Next Course: "
            f"{next_course['name']}"
        )

    else:

        print(
            "\n  🎉 No pending recommended course."
        )

    # --------------------------------------------------------
    # VERIFIED SKILLS
    # --------------------------------------------------------

    verified_skills = get_verified_skills(
        skill_scores
    )

    print("\n🏆 VERIFIED SKILLS")
    print("-" * 60)

    if verified_skills:

        for skill in verified_skills:

            print(
                f"  ✓ {skill}"
            )

    else:

        print(
            "  No verified skills yet."
        )

    print("\n" + "═" * 60)
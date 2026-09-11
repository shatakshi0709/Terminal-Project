from utils.storage import (
    save_candidate,
    load_candidates,
    update_candidate_scores,
    update_learning_progress
)

from engine.diagnostic import (
    start_diagnostic,
    calculate_skill_scores,
    show_results
)

from engine.scoring import (
    calculate_weighted_score,
    get_readiness_level
)

from engine.skill_gap import (
    calculate_skill_gaps,
    show_skill_gaps
)

from engine.recommender import (
    recommend_jobs,
    get_job_by_title,
    load_jobs
)

from engine.learning_path import (
    recommend_courses,
    show_learning_path,
    update_course_status
)


# ============================================================
# UI HELPERS
# ============================================================

def display_header():

    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + "SMART CAREER ENGINE".center(58) + "║")
    print("║" + "Competency • Career • Learning".center(58) + "║")
    print("╚" + "═" * 58 + "╝")


def display_menu():

    print("\n┌──────────────────── MAIN MENU ────────────────────┐")
    print("│                                                  │")
    print("│  1. 👤 Create Candidate Profile                 │")
    print("│  2. 📝 Take Competency Diagnostic               │")
    print("│  3. 📊 View My Skill Scores                     │")
    print("│  4. 💼 Find Suitable Jobs                       │")
    print("│  5. 🔍 Analyze Skill Gaps                       │")
    print("│  6. 📚 Get Personalized Learning Path           │")
    print("│  7. 🎯 Career Readiness                          │")
    print("│  8. 📈 Track Learning Progress                  │")
    print("│  9. 🚪 Exit                                     │")
    print("│                                                  │")
    print("└──────────────────────────────────────────────────┘")


def pause():

    input("\nPress Enter to continue...")


# ============================================================
# CANDIDATE PROFILE
# ============================================================

def create_profile():

    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + "CREATE CANDIDATE PROFILE".center(58) + "║")
    print("╚" + "═" * 58 + "╝")

    name = input("\n👤 Name: ").strip()

    education = input("🎓 Education: ").strip()

    experience = input("💼 Experience: ").strip()

    jobs = load_jobs()

    print("\n🎯 AVAILABLE JOB ROLES")
    print("-" * 50)

    for index, job in enumerate(jobs, start=1):

        print(
            f"  {index}. {job['title']}"
        )

    while True:

        choice = input(
            "\nSelect your target role (1-{}): ".format(
                len(jobs)
            )
        ).strip()

        if choice.isdigit():

            role_index = int(choice)

            if 1 <= role_index <= len(jobs):

                target_role = jobs[
                    role_index - 1
                ]["title"]

                break

        print(
            "⚠ Invalid selection. "
            "Please choose a valid number."
        )

    location = input(
        "📍 Preferred Location: "
    ).strip()

    profile = {

        "name": name,

        "education": education,

        "experience": experience,

        "target_role": target_role,

        "location": location

    }

    save_candidate(profile)

    print("\n")
    print("╔" + "═" * 58 + "╗")
    print(
        "║" +
        "✓ PROFILE CREATED SUCCESSFULLY".center(58) +
        "║"
    )
    print("╚" + "═" * 58 + "╝")

    print(
        f"\n  👤 Candidate : {name}"
    )

    print(
        f"  🎓 Education : {education}"
    )

    print(
        f"  💼 Experience: {experience}"
    )

    print(
        f"  🎯 Target Role: {target_role}"
    )

    print(
        f"  📍 Location  : {location}"
    )

    return profile


# ============================================================
# VIEW SKILLS
# ============================================================

def show_my_skills(skill_scores):

    print("\n")
    print("╔" + "═" * 58 + "╗")
    print(
        "║" +
        "MY SKILL SCORES".center(58) +
        "║"
    )
    print("╚" + "═" * 58 + "╝")

    for skill, score in skill_scores.items():

        filled = score // 10

        empty = 10 - filled

        bar = (
            "█" * filled +
            "░" * empty
        )

        print(
            f"\n  {skill:<18}"
            f"{bar} {score}%"
        )

    print(
        "\n" + "─" * 60
    )


# ============================================================
# JOB RECOMMENDATION
# ============================================================

def display_job_summary(recommendations):

    print("\n")
    print("╔" + "═" * 58 + "╗")
    print(
        "║" +
        "TOP JOB RECOMMENDATIONS".center(58) +
        "║"
    )
    print("╚" + "═" * 58 + "╝")

    if not recommendations:

        print(
            "\n  No suitable jobs found."
        )

        print(
            "\n" + "─" * 60
        )

        return

    for index, job in enumerate(
        recommendations,
        start=1
    ):

        print(
            f"\n  {index}. {job['title']}"
        )

        print(
            f"     Match      : "
            f"{job['score']}%"
        )

        print(
            f"     Salary     : "
            f"{job['salary']}"
        )

        print(
            f"     Experience : "
            f"{job['experience']}"
        )

    print(
        "\n" + "─" * 60
    )


# ============================================================
# LEARNING PROGRESS
# ============================================================

def track_learning_progress(
    profile,
    skill_scores
):

    if not skill_scores:

        print(
            "\n⚠ Please take the competency "
            "diagnostic first."
        )

        return None

    target_job = get_job_by_title(
        profile["target_role"]
    )

    if not target_job:

        print(
            "\n⚠ Target job role not found."
        )

        return None

    gaps = calculate_skill_gaps(
        skill_scores,
        target_job["requirements"]
    )

    recommendations = recommend_courses(
        gaps
    )

    learning_progress = profile.get(
        "learning_progress",
        {}
    )

    if not recommendations:

        print(
            "\n🎉 No learning gaps found."
        )

        return learning_progress

    # Show current progress
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print(
        "║" +
        "LEARNING PROGRESS TRACKER".center(58) +
        "║"
    )
    print("╚" + "═" * 58 + "╝")

    course_list = []

    number = 1

    for recommendation in recommendations:

        for course in recommendation["courses"]:

            course_list.append(
                course["name"]
            )

            status = learning_progress.get(
                course["name"],
                "Not Started"
            )

            print(
                f"\n  {number}. 📘 "
                f"{course['name']}"
            )

            print(
                f"     Skill: "
                f"{course['skill']}"
            )

            print(
                f"     Status: "
                f"{status}"
            )

            number += 1

    if not course_list:

        print(
            "\n⚠ No courses available "
            "for your current skill gaps."
        )

        return learning_progress

    print("\n" + "─" * 60)

    while True:

        choice = input(
            "\nSelect course number "
            "(0 to go back): "
        ).strip()

        if choice == "0":

            break

        if not choice.isdigit():

            print(
                "⚠ Please enter a valid number."
            )

            continue

        course_index = int(choice)

        if not (
            1 <= course_index <= len(course_list)
        ):

            print(
                "⚠ Invalid course number."
            )

            continue

        course_name = course_list[
            course_index - 1
        ]

        print(
            "\nSelect status:"
        )

        print(
            "  1. 🟡 Not Started"
        )

        print(
            "  2. 🔵 In Progress"
        )

        print(
            "  3. 🟢 Completed"
        )

        status_choice = input(
            "\nEnter status: "
        ).strip()

        status_map = {

            "1": "Not Started",

            "2": "In Progress",

            "3": "Completed"

        }

        if status_choice not in status_map:

            print(
                "⚠ Invalid status."
            )

            continue

        new_status = status_map[
            status_choice
        ]

        learning_progress = update_course_status(
            learning_progress,
            course_name,
            new_status
        )

        update_learning_progress(
            profile["name"],
            learning_progress
        )

        profile[
            "learning_progress"
        ] = learning_progress

        print(
            f"\n✓ {course_name}"
        )

        print(
            f"  Status updated to: "
            f"{new_status}"
        )

    return learning_progress


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    candidates = load_candidates()

    if candidates:

        profile = candidates[-1]

        skill_scores = profile.get(
            "skill_scores",
            {}
        )

    else:

        profile = None

        skill_scores = {}

    while True:

        display_header()

        if profile:

            print(
                f"\n  👤 {profile['name']}"
                f"   |   🎯 "
                f"{profile['target_role']}"
            )

        display_menu()

        choice = input(
            "\nEnter your choice: "
        ).strip()

        # ====================================================
        # 1. CREATE PROFILE
        # ====================================================

        if choice == "1":

            profile = create_profile()

            skill_scores = {}

            pause()

        # ====================================================
        # 2. DIAGNOSTIC
        # ====================================================

        elif choice == "2":

            if not profile:

                print(
                    "\n⚠ Please create your "
                    "candidate profile first."
                )

                pause()

                continue

            print(
                "\nStarting competency diagnostic..."
            )

            scores = start_diagnostic()

            skill_scores = calculate_skill_scores(
                scores
            )

            update_candidate_scores(
                profile["name"],
                skill_scores
            )

            profile[
                "skill_scores"
            ] = skill_scores

            show_results(
                skill_scores
            )

            pause()

        # ====================================================
        # 3. VIEW SKILLS
        # ====================================================

        elif choice == "3":

            if not skill_scores:

                print(
                    "\n⚠ Please take the competency "
                    "diagnostic first."
                )

                pause()

                continue

            show_my_skills(
                skill_scores
            )

            pause()

        # ====================================================
        # 4. JOB RECOMMENDATION
        # ====================================================

        elif choice == "4":

            if not skill_scores:

                print(
                    "\n⚠ Please take the competency "
                    "diagnostic first."
                )

                pause()

                continue

            recommendations = recommend_jobs(
                skill_scores
            )

            display_job_summary(
                recommendations
            )

            pause()

        # ====================================================
        # 5. SKILL GAP
        # ====================================================

        elif choice == "5":

            if not profile:

                print(
                    "\n⚠ Please create your "
                    "candidate profile first."
                )

                pause()

                continue

            if not skill_scores:

                print(
                    "\n⚠ Please take the competency "
                    "diagnostic first."
                )

                pause()

                continue

            target_job = get_job_by_title(
                profile["target_role"]
            )

            if not target_job:

                print(
                    "\n⚠ Target job role not found."
                )

                pause()

                continue

            gaps = calculate_skill_gaps(
                skill_scores,
                target_job["requirements"]
            )

            print(
                f"\n🎯 Target Role: "
                f"{target_job['title']}"
            )

            show_skill_gaps(
                gaps
            )

            pause()

        # ====================================================
        # 6. LEARNING PATH
        # ====================================================

        elif choice == "6":

            if not profile:

                print(
                    "\n⚠ Please create your "
                    "candidate profile first."
                )

                pause()

                continue

            if not skill_scores:

                print(
                    "\n⚠ Please take the competency "
                    "diagnostic first."
                )

                pause()

                continue

            target_job = get_job_by_title(
                profile["target_role"]
            )

            if not target_job:

                print(
                    "\n⚠ Target job role not found."
                )

                pause()

                continue

            gaps = calculate_skill_gaps(
                skill_scores,
                target_job["requirements"]
            )

            recommendations = recommend_courses(
                gaps
            )

            learning_progress = profile.get(
                "learning_progress",
                {}
            )

            print(
                f"\n🎯 Target Role: "
                f"{target_job['title']}"
            )

            show_learning_path(
                recommendations,
                learning_progress
            )

            pause()

        # ====================================================
        # 7. CAREER READINESS
        # ====================================================

        elif choice == "7":

            if not profile:

                print(
                    "\n⚠ Please create your "
                    "candidate profile first."
                )

                pause()

                continue

            if not skill_scores:

                print(
                    "\n⚠ Please take the competency "
                    "diagnostic first."
                )

                pause()

                continue

            target_job = get_job_by_title(
                profile["target_role"]
            )

            if not target_job:

                print(
                    "\n⚠ Target job role not found."
                )

                pause()

                continue

            score = calculate_weighted_score(
                skill_scores,
                target_job["weights"]
            )

            print("\n")
            print("╔" + "═" * 58 + "╗")
            print(
                "║" +
                "CAREER READINESS".center(58) +
                "║"
            )
            print("╚" + "═" * 58 + "╝")

            print(
                f"\n  🎯 Target Role"
                f"        : "
                f"{target_job['title']}"
            )

            print(
                f"  📊 Readiness Score"
                f"      : {score}%"
            )

            print(
                f"  🚦 Status"
                f"              : "
                f"{get_readiness_level(score)}"
            )

            print(
                "\n" + "─" * 60
            )

            if score >= 80:

                print(
                    "  🎉 You are ready "
                    "to apply for this role!"
                )

            elif score >= 65:

                print(
                    "  💪 You are close! "
                    "Focus on your skill gaps."
                )

            elif score >= 50:

                print(
                    "  📚 Keep learning "
                    "and improving your skills."
                )

            else:

                print(
                    "  🚀 Upskilling is recommended "
                    "before applying."
                )

            print(
                "\n" + "═" * 60
            )

            pause()

        # ====================================================
        # 8. LEARNING PROGRESS
        # ====================================================

        elif choice == "8":

            if not profile:

                print(
                    "\n⚠ Please create your "
                    "candidate profile first."
                )

                pause()

                continue

            track_learning_progress(
                profile,
                skill_scores
            )

            pause()

        # ====================================================
        # 9. EXIT
        # ====================================================

        elif choice == "9":

            print("\n")
            print("╔" + "═" * 58 + "╗")
            print(
                "║" +
                "THANK YOU FOR USING".center(58) +
                "║"
            )

            print(
                "║" +
                "SMART CAREER ENGINE 🚀".center(58) +
                "║"
            )

            print("╚" + "═" * 58 + "╝")

            print(
                "\n  Keep learning. "
                "Keep growing. "
                "Keep building! 💙\n"
            )

            break

        # ====================================================
        # INVALID OPTION
        # ====================================================

        else:

            print(
                "\n⚠ Invalid choice. "
                "Please select 1-9."
            )

            pause()


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    main()
from utils.storage import (
    save_candidate,
    load_candidates,
    update_candidate_scores
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
    show_learning_path
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
    print("│  8. 🚪 Exit                                     │")
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

    # ----------------------------------------
    # JOB ROLE SELECTION
    # ----------------------------------------

    jobs = load_jobs()

    print("\n🎯 AVAILABLE JOB ROLES")
    print("-" * 50)

    for index, job in enumerate(jobs, start=1):
        print(f"  {index}. {job['title']}")

    while True:

        choice = input(
            "\nSelect your target role (1-{}): ".format(len(jobs))
        ).strip()

        if choice.isdigit():

            role_index = int(choice)

            if 1 <= role_index <= len(jobs):

                target_role = jobs[role_index - 1]["title"]

                break

        print("⚠ Invalid selection. Please choose a valid number.")

    location = input("📍 Preferred Location: ").strip()

    profile = {
        "name": name,
        "education": education,
        "experience": experience,
        "target_role": target_role,
        "location": location
    }

    # Save profile
    save_candidate(profile)

    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + "✓ PROFILE CREATED SUCCESSFULLY".center(58) + "║")
    print("╚" + "═" * 58 + "╝")

    print(f"\n  👤 Candidate : {name}")
    print(f"  🎓 Education : {education}")
    print(f"  💼 Experience: {experience}")
    print(f"  🎯 Target Role: {target_role}")
    print(f"  📍 Location  : {location}")

    return profile


# ============================================================
# VIEW SKILLS
# ============================================================

def show_my_skills(skill_scores):

    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + "MY SKILL SCORES".center(58) + "║")
    print("╚" + "═" * 58 + "╝")

    for skill, score in skill_scores.items():

        filled = score // 10
        empty = 10 - filled

        bar = "█" * filled + "░" * empty

        print(
            f"\n  {skill:<18} "
            f"{bar} {score}%"
        )

    print("\n" + "─" * 60)


# ============================================================
# JOB RECOMMENDATION
# ============================================================

def display_job_summary(recommendations):

    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + "TOP JOB RECOMMENDATIONS".center(58) + "║")
    print("╚" + "═" * 58 + "╝")

    if not recommendations:

        print("\n  No suitable jobs found.")

        print("\n" + "─" * 60)

        return

    for index, job in enumerate(
        recommendations,
        start=1
    ):

        print(
            f"\n  {index}. {job['title']}"
        )

        print(
            f"     Match      : {job['score']}%"
        )

        print(
            f"     Salary     : {job['salary']}"
        )

        print(
            f"     Experience : {job['experience']}"
        )

    print("\n" + "─" * 60)


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    # Load previously saved candidates
    candidates = load_candidates()

    # Load latest candidate profile
    if candidates:

        profile = candidates[-1]

        # Load previously saved skill scores
        skill_scores = profile.get(
            "skill_scores",
            {}
        )

    else:

        profile = None
        skill_scores = {}

    # ========================================================
    # MAIN LOOP
    # ========================================================

    while True:

        display_header()

        # ----------------------------------------
        # SHOW CURRENT CANDIDATE
        # ----------------------------------------

        if profile:

            print(
                f"\n  👤 {profile['name']}"
                f"   |   🎯 {profile['target_role']}"
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

            # New profile has no diagnostic scores yet
            skill_scores = {}

            pause()

        # ====================================================
        # 2. DIAGNOSTIC
        # ====================================================

        elif choice == "2":

            if not profile:

                print(
                    "\n⚠ Please create your candidate profile first."
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

            # Save scores to candidates.json
            update_candidate_scores(
                profile["name"],
                skill_scores
            )

            # Update current profile in memory
            profile["skill_scores"] = skill_scores

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
                    "\n⚠ Please take the competency diagnostic first."
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
                    "\n⚠ Please take the competency diagnostic first."
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
                    "\n⚠ Please create your candidate profile first."
                )

                pause()

                continue

            if not skill_scores:

                print(
                    "\n⚠ Please take the competency diagnostic first."
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
                    "\n⚠ Please create your candidate profile first."
                )

                pause()

                continue

            if not skill_scores:

                print(
                    "\n⚠ Please take the competency diagnostic first."
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

            print(
                f"\n🎯 Target Role: "
                f"{target_job['title']}"
            )

            show_learning_path(
                recommendations
            )

            pause()

        # ====================================================
        # 7. CAREER READINESS
        # ====================================================

        elif choice == "7":

            if not profile:

                print(
                    "\n⚠ Please create your candidate profile first."
                )

                pause()

                continue

            if not skill_scores:

                print(
                    "\n⚠ Please take the competency diagnostic first."
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
            print("║" + "CAREER READINESS".center(58) + "║")
            print("╚" + "═" * 58 + "╝")

            print(
                f"\n  🎯 Target Role"
                f"        : {target_job['title']}"
            )

            print(
                f"  📊 Readiness Score"
                f"      : {score}%"
            )

            print(
                f"  🚦 Status"
                f"              : {get_readiness_level(score)}"
            )

            print("\n" + "─" * 60)

            if score >= 80:

                print(
                    "  🎉 You are ready to apply for this role!"
                )

            elif score >= 65:

                print(
                    "  💪 You are close! Focus on your skill gaps."
                )

            elif score >= 50:

                print(
                    "  📚 Keep learning and improving your skills."
                )

            else:

                print(
                    "  🚀 Upskilling is recommended before applying."
                )

            print("\n" + "═" * 60)

            pause()

        # ====================================================
        # 8. EXIT
        # ====================================================

        elif choice == "8":

            print("\n")
            print("╔" + "═" * 58 + "╗")
            print("║" + "THANK YOU FOR USING".center(58) + "║")
            print("║" + "SMART CAREER ENGINE 🚀".center(58) + "║")
            print("╚" + "═" * 58 + "╝")

            print(
                "\n  Keep learning. Keep growing. Keep building! 💙\n"
            )

            break

        # ====================================================
        # INVALID OPTION
        # ====================================================

        else:

            print(
                "\n⚠ Invalid choice. Please select 1-8."
            )

            pause()


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    main()
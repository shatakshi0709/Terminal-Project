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
    show_recommendations
)

from engine.learning_path import (
    recommend_courses,
    show_learning_path
)


def display_header():

    print("\n" + "=" * 60)
    print("              SMART CAREER ENGINE")
    print("       Competency • Career • Learning")
    print("=" * 60)


def display_menu():

    print("\n1. Create Candidate Profile")
    print("2. Take Competency Diagnostic")
    print("3. View My Skill Scores")
    print("4. Find Suitable Jobs")
    print("5. Analyze Skill Gaps")
    print("6. Get Personalized Learning Path")
    print("7. Career Readiness")
    print("8. Exit")


def create_profile():

    print("\n" + "-" * 50)
    print("          CREATE CANDIDATE PROFILE")
    print("-" * 50)

    name = input("Name: ")
    education = input("Education: ")
    experience = input("Experience: ")
    target_role = input("Target Job Role: ")
    location = input("Preferred Location: ")

    profile = {
        "name": name,
        "education": education,
        "experience": experience,
        "target_role": target_role,
        "location": location
    }

    print("\n✓ Profile created successfully!")

    print(f"\nCandidate: {name}")
    print(f"Target Role: {target_role}")

    return profile


def main():

    profile = None
    skill_scores = {}

    while True:

        display_header()

        if profile:

            print(f"\nCandidate: {profile['name']}")
            print(f"Target Role: {profile['target_role']}")

        display_menu()

        choice = input("\nEnter your choice: ").strip()

        # -----------------------------------
        # CREATE PROFILE
        # -----------------------------------

        if choice == "1":

            profile = create_profile()

        # -----------------------------------
        # DIAGNOSTIC
        # -----------------------------------

        elif choice == "2":

            if not profile:

                print("\n⚠ Please create your profile first.")

                continue

            scores = start_diagnostic()

            skill_scores = calculate_skill_scores(scores)

            show_results(skill_scores)

        # -----------------------------------
        # VIEW SKILLS
        # -----------------------------------

        elif choice == "3":

            if not skill_scores:

                print("\n⚠ Please take the competency diagnostic first.")

                continue

            print("\n" + "=" * 50)
            print("             MY SKILL SCORES")
            print("=" * 50)

            for skill, score in skill_scores.items():

                print(f"{skill:<20} {score}%")

        # -----------------------------------
        # JOB RECOMMENDATION
        # -----------------------------------

        elif choice == "4":

            if not skill_scores:

                print("\n⚠ Please take the competency diagnostic first.")

                continue

            recommendations = recommend_jobs(
                skill_scores
            )

            show_recommendations(
                recommendations
            )

        # -----------------------------------
        # SKILL GAP
        # -----------------------------------

        elif choice == "5":

            if not skill_scores:

                print("\n⚠ Please take the competency diagnostic first.")

                continue

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

        # -----------------------------------
        # LEARNING PATH
        # -----------------------------------

        elif choice == "6":

            if not skill_scores:

                print("\n⚠ Please take the competency diagnostic first.")

                continue

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

            recommendations = recommend_courses(
                gaps
            )

            show_learning_path(
                recommendations
            )

        # -----------------------------------
        # CAREER READINESS
        # -----------------------------------

        elif choice == "7":

            if not skill_scores:

                print("\n⚠ Please take the competency diagnostic first.")

                continue

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

            print("\n" + "=" * 50)
            print("             CAREER READINESS")
            print("=" * 50)

            print(f"\nCareer Readiness Score: {score}%")
            print(f"Status: {get_readiness_level(score)}")

            print("=" * 50)

        # -----------------------------------
        # EXIT
        # -----------------------------------

        elif choice == "8":

            print("\nThank you for using Smart Career Engine! 🚀")

            break

        else:

            print("\n⚠ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
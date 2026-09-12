def get_verification_status(score):

    if score >= 75:
        return "VERIFIED 🟢"

    elif score >= 50:
        return "DEVELOPING 🟡"

    else:
        return "NOT VERIFIED 🔴"


def get_verified_skills(skill_scores):

    verified = []

    for skill, score in skill_scores.items():

        if score >= 75:
            verified.append(skill)

    return verified


def show_skill_verification(skill_scores):

    print("\n")
    print("╔" + "═" * 58 + "╗")
    print(
        "║" +
        "SKILL VERIFICATION & CERTIFICATION".center(58) +
        "║"
    )
    print("╚" + "═" * 58 + "╝")

    if not skill_scores:

        print(
            "\n⚠ Please take the competency diagnostic first."
        )

        return

    for skill, score in skill_scores.items():

        status = get_verification_status(score)

        print(
            f"\n  🧠 {skill}"
        )

        print(
            f"     Score  : {score}%"
        )

        print(
            f"     Status : {status}"
        )

    verified_skills = get_verified_skills(
        skill_scores
    )

    print("\n" + "-" * 60)

    if verified_skills:

        print("\n🏆 VERIFIED SKILLS")

        for skill in verified_skills:

            print(
                f"   ✓ {skill}"
            )

        print(
            "\n🎖 Candidate is eligible for "
            "skill verification badges."
        )

    else:

        print(
            "\n📚 No skills have reached the "
            "verification threshold yet."
        )

    print("\n" + "═" * 60)
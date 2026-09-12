import json


def load_questions():
    with open("data/questions.json", "r") as file:
        return json.load(file)


def reassess_skill(skill):
    questions = load_questions()

    skill_questions = [
        question
        for question in questions
        if question["skill"] == skill
    ]

    if not skill_questions:
        print("\n⚠ No assessment available for this skill.")
        return None

    correct = 0

    print("\n" + "=" * 60)
    print(f"        RE-ASSESSMENT: {skill}")
    print("=" * 60)

    for index, question in enumerate(skill_questions, start=1):

        print("\n" + "-" * 60)
        print(f"Question {index}/{len(skill_questions)}")
        print(question["question"])
        print()

        for option, value in question["options"].items():
            print(f"{option}. {value}")

        while True:
            answer = input("\nYour answer: ").strip().upper()

            if answer in ["A", "B", "C", "D"]:
                break

            print("⚠ Please enter A, B, C or D.")

        if answer == question["answer"]:
            correct += 1
            print("✓ Correct!")
        else:
            print(
                f"✗ Incorrect! "
                f"Correct answer: {question['answer']}"
            )

    new_score = round(
        (correct / len(skill_questions)) * 100
    )

    print("\n" + "=" * 60)
    print(f"Updated {skill} Score: {new_score}%")
    print("=" * 60)

    return new_score


def update_skill_after_reassessment(
    skill_scores,
    skill,
    new_score
):
    skill_scores[skill] = new_score
    return skill_scores
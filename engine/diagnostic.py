import json


def load_questions():
    with open("data/questions.json", "r") as file:
        return json.load(file)


def start_diagnostic():
    questions = load_questions()

    scores = {}

    print("\n" + "=" * 50)
    print("          COMPETENCY DIAGNOSTIC")
    print("=" * 50)

    print(f"\nTotal Questions: {len(questions)}")
    print("Answer each question using A, B, C or D.\n")

    for i, question in enumerate(questions, start=1):

        print("-" * 50)
        print(f"Question {i}/{len(questions)}")
        print(f"Skill: {question['skill']}")
        print()
        print(question["question"])
        print()

        for option, value in question["options"].items():
            print(f"{option}. {value}")

        while True:
            answer = input("\nYour answer: ").strip().upper()

            if answer in ["A", "B", "C", "D"]:
                break

            print("Invalid answer. Please enter A, B, C or D.")

        skill = question["skill"]

        if skill not in scores:
            scores[skill] = {
                "correct": 0,
                "total": 0
            }

        scores[skill]["total"] += 1

        if answer == question["answer"]:
            scores[skill]["correct"] += 1
            print("✓ Correct!")
        else:
            print(f"✗ Incorrect! Correct answer: {question['answer']}")

    return scores


def calculate_skill_scores(scores):
    skill_scores = {}

    for skill, data in scores.items():
        percentage = (data["correct"] / data["total"]) * 100
        skill_scores[skill] = round(percentage)

    return skill_scores


def show_results(skill_scores):

    print("\n")
    print("=" * 50)
    print("             DIAGNOSTIC RESULT")
    print("=" * 50)

    for skill, score in skill_scores.items():

        if score >= 75:
            level = "Strong 🟢"
        elif score >= 50:
            level = "Developing 🟡"
        else:
            level = "Needs Improvement 🔴"

        print(f"\n{skill:<20} {score:>3}%   {level}")

    overall_score = round(
        sum(skill_scores.values()) / len(skill_scores)
    )

    print("\n" + "-" * 50)
    print(f"Overall Competency Score: {overall_score}%")

    if overall_score >= 75:
        print("Readiness Level: JOB READY 🟢")
    elif overall_score >= 50:
        print("Readiness Level: DEVELOPING 🟡")
    else:
        print("Readiness Level: NEEDS UPSKILLING 🔴")

    print("=" * 50)


if __name__ == "__main__":

    scores = start_diagnostic()

    skill_scores = calculate_skill_scores(scores)

    show_results(skill_scores)
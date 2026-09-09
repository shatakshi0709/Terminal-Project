import json

from engine.scoring import calculate_weighted_score


def load_jobs():
    with open("data/jobs.json", "r") as file:
        return json.load(file)


def calculate_job_match(skill_scores, job):

    score = calculate_weighted_score(
        skill_scores,
        job["weights"]
    )

    return score


def recommend_jobs(skill_scores):

    jobs = load_jobs()

    recommendations = []

    for job in jobs:

        score = calculate_job_match(
            skill_scores,
            job
        )

        recommendations.append({
            "title": job["title"],
            "score": score,
            "salary": job["salary"],
            "requirements": job["requirements"]
        })

    recommendations.sort(
        key=lambda job: job["score"],
        reverse=True
    )

    return recommendations


def show_recommendations(recommendations):

    print("\n" + "=" * 65)
    print("              RECOMMENDED CAREER PATHS")
    print("=" * 65)

    for index, job in enumerate(recommendations, start=1):

        print(
            f"\n{index}. {job['title']}"
        )

        print(
            f"   Compatibility: {job['score']}%"
        )

        print(
            f"   Salary Range: {job['salary']}"
        )

    print("\n" + "=" * 65)


# TESTING
if __name__ == "__main__":

    skill_scores = {
        "Python": 100,
        "SQL": 100,
        "DSA": 50,
        "Backend": 100,
        "System Design": 0
    }

    recommendations = recommend_jobs(
        skill_scores
    )

    show_recommendations(
        recommendations
    )
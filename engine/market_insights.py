import json


def load_market_jobs():
    with open("data/jobs.json", "r") as file:
        return json.load(file)


def calculate_skill_demand(jobs):
    skill_demand = {}

    for job in jobs:

        for skill, requirement in job["requirements"].items():

            if requirement >= 60:
                skill_demand[skill] = (
                    skill_demand.get(skill, 0) + 1
                )

    return skill_demand


def get_salary_number(salary):

    try:
        salary = salary.replace("₹", "")
        salary = salary.replace(" LPA", "")

        minimum, maximum = salary.split("-")

        return float(minimum), float(maximum)

    except:
        return 0, 0


def calculate_salary_benchmarks(jobs):

    salary_data = []

    for job in jobs:

        minimum, maximum = get_salary_number(
            job["salary"]
        )

        salary_data.append({
            "title": job["title"],
            "min_salary": minimum,
            "max_salary": maximum
        })

    return salary_data


def show_market_insights():

    jobs = load_market_jobs()

    skill_demand = calculate_skill_demand(jobs)

    salary_data = calculate_salary_benchmarks(jobs)

    print("\n")
    print("╔" + "═" * 58 + "╗")
    print(
        "║" +
        "JOB MARKET INSIGHTS".center(58) +
        "║"
    )
    print("╚" + "═" * 58 + "╝")

    print("\n🔥 IN-DEMAND SKILLS")
    print("-" * 60)

    sorted_skills = sorted(
        skill_demand.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for skill, demand in sorted_skills:

        print(
            f"  {skill:<20} "
            f"Demand: {demand} job roles"
        )

    print("\n💼 AVAILABLE JOB ROLES")
    print("-" * 60)

    for job in jobs:

        print(
            f"  • {job['title']:<30}"
            f"{job['salary']}"
        )

    print("\n💰 SALARY BENCHMARKS")
    print("-" * 60)

    for salary in salary_data:

        print(
            f"  {salary['title']:<30}"
            f"₹{salary['min_salary']:.0f}-"
            f"{salary['max_salary']:.0f} LPA"
        )

    print("\n" + "═" * 60)
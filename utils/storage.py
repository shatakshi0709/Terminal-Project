import json


def save_candidate(candidate):

    try:
        with open("data/candidates.json", "r") as file:
            candidates = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):

        candidates = []

    candidates.append(candidate)

    with open("data/candidates.json", "w") as file:

        json.dump(
            candidates,
            file,
            indent=4
        )


def load_candidates():

    try:

        with open("data/candidates.json", "r") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):

        return []


def update_candidate_scores(name, skill_scores):

    candidates = load_candidates()

    for candidate in reversed(candidates):

        if candidate["name"] == name:

            candidate["skill_scores"] = skill_scores

            break

    with open("data/candidates.json", "w") as file:

        json.dump(
            candidates,
            file,
            indent=4
        )


def update_learning_progress(name, learning_progress):

    candidates = load_candidates()

    for candidate in reversed(candidates):

        if candidate["name"] == name:

            candidate["learning_progress"] = learning_progress

            break

    with open("data/candidates.json", "w") as file:

        json.dump(
            candidates,
            file,
            indent=4
        )
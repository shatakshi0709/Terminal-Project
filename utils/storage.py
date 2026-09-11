import json


def save_candidate(candidate):
    try:
        with open("data/candidates.json", "r") as file:
            candidates = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        candidates = []

    candidates.append(candidate)

    with open("data/candidates.json", "w") as file:
        json.dump(candidates, file, indent=4)


def load_candidates():
    try:
        with open("data/candidates.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
import json
import os

SAVE_DIR = "saves"


def save_slot(cells, slot):
    os.makedirs(SAVE_DIR, exist_ok=True)
    with open(os.path.join(SAVE_DIR, f"slot_{slot}.json"), "w") as f:
        json.dump(cells, f)


def load_slot(slot):
    path = os.path.join(SAVE_DIR, f"slot_{slot}.json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def slot_exists(slot):
    return os.path.exists(os.path.join(SAVE_DIR, f"slot_{slot}.json"))

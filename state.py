import json
import os

SAVE_DIR = "saves"


def save_slot(cells: list[list[bool]], slot: int) -> None:
    os.makedirs(SAVE_DIR, exist_ok=True)
    with open(os.path.join(SAVE_DIR, f"slot_{slot}.json"), "w") as f:
        json.dump(cells, f)


def load_slot(slot: int) -> list[list[bool]] | None:
    path = os.path.join(SAVE_DIR, f"slot_{slot}.json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def slot_exists(slot: int) -> bool:
    return os.path.exists(os.path.join(SAVE_DIR, f"slot_{slot}.json"))

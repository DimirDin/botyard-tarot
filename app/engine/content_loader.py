"""
Loads the static tarot content database straight from versioned JSON files
under content/. We deliberately do NOT load this content into Postgres:
it never needs relational queries, it's versioned with the code, and reading
it directly keeps deploys simple (see PROJECT_CONTEXT.md "Content storage
decision"). Only `users` and `readings` (which reference a rendered snapshot,
not a live pointer into this content) live in Postgres.
"""
import json
import functools
from pathlib import Path
from typing import Dict, Any, List

from app.config import CONTENT_DIR

CARDS_DIR = CONTENT_DIR / "cards"
THEMES = ("general", "love", "career", "finance", "health", "spirit")
SPREADS = ("one_card", "three_card", "celtic_cross")


@functools.lru_cache(maxsize=1)
def load_all_cards() -> Dict[str, Dict[str, Any]]:
    cards = {}
    for path in sorted(CARDS_DIR.glob("*.json")):
        if path.name.startswith("_"):
            continue
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        cards[data["id"]] = data
    if len(cards) != 78:
        raise RuntimeError(f"Expected 78 cards, found {len(cards)} in {CARDS_DIR}")
    return cards


@functools.lru_cache(maxsize=1)
def load_position_nuance() -> Dict[str, Any]:
    with open(CONTENT_DIR / "position_nuance.json", encoding="utf-8") as f:
        return json.load(f)


@functools.lru_cache(maxsize=1)
def load_combinations() -> Dict[str, Any]:
    with open(CONTENT_DIR / "combinations.json", encoding="utf-8") as f:
        return json.load(f)["combinations"]


def get_card(card_id: str) -> Dict[str, Any]:
    return load_all_cards()[card_id]


def all_card_ids() -> List[str]:
    return list(load_all_cards().keys())


def combination_key(id_a: str, id_b: str) -> str:
    a, b = sorted([id_a, id_b])
    return f"{a}|{b}"


def find_combination(card_ids: List[str]):
    """Return combination notes for every pair among the drawn cards that has an entry."""
    combos = load_combinations()
    notes = []
    for i in range(len(card_ids)):
        for j in range(i + 1, len(card_ids)):
            key = combination_key(card_ids[i], card_ids[j])
            if key in combos:
                notes.append(combos[key]["text"])
    return notes

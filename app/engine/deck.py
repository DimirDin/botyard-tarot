"""Deterministic-shape (but randomly drawn) tarot deck mechanics.

78 cards, each drawn card lands upright or reversed with no repeats within
one spread. Position labels come from content/position_nuance.json so the
same code serves 1-card, 3-card and Celtic Cross spreads without change.
"""
import random
from dataclasses import dataclass
from typing import List

from app.engine.content_loader import all_card_ids

SPREAD_POSITIONS = {
    "one_card": 1,
    "three_card": 3,
    "celtic_cross": 10,
}


@dataclass
class DrawnCard:
    card_id: str
    upright: bool
    position: int  # 0-based index into the spread's position list


def draw_spread(spread_type: str, rng: random.Random = None) -> List[DrawnCard]:
    if spread_type not in SPREAD_POSITIONS:
        raise ValueError(f"Unknown spread_type: {spread_type}")
    n = SPREAD_POSITIONS[spread_type]
    rng = rng or random.Random()
    pool = all_card_ids()
    chosen = rng.sample(pool, n)
    drawn = []
    for i, card_id in enumerate(chosen):
        upright = rng.random() >= 0.5
        drawn.append(DrawnCard(card_id=card_id, upright=upright, position=i))
    return drawn

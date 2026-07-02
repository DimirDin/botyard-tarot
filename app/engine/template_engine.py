"""
The deterministic template engine: given a card id, orientation, theme,
spread type, position index and the full set of drawn cards (for combination
lookups), assemble ONE coherent reading paragraph for that card.

Determinism requirement (see PROJECT_CONTEXT.md "verify with a script"):
same (card_id, theme, orientation, spread_type, position, other_card_ids)
-> byte-identical output, always. No randomness happens in this module —
all randomness (which card, which orientation) happens earlier in deck.py.
"""
from typing import List, Optional
from dataclasses import dataclass

from app.engine.content_loader import get_card, load_position_nuance, find_combination

VALID_THEMES = ("general", "love", "career", "finance", "health", "spirit")


@dataclass
class AssembledCard:
    card_id: str
    name_ru: str
    upright: bool
    position: int
    position_label: Optional[str]
    text: str
    yes_no: Optional[str]


def _orientation_key(upright: bool) -> str:
    return "upright" if upright else "reversed"


def assemble_card_reading(
    card_id: str,
    upright: bool,
    theme: str,
    spread_type: str,
    position: int,
    other_card_ids: Optional[List[str]] = None,
) -> AssembledCard:
    if theme not in VALID_THEMES:
        raise ValueError(f"Unknown theme: {theme}")
    card = get_card(card_id)
    ori = _orientation_key(upright)

    base = card["meanings"][theme][ori]
    advice = card["advice"][ori]

    nuance_map = load_position_nuance().get(spread_type, {})
    nuance_entry = nuance_map.get(str(position))
    position_label = nuance_entry["label"] if nuance_entry else None

    paragraphs = [base]

    if nuance_entry:
        paragraphs.append(nuance_entry["text"])

    other_card_ids = other_card_ids or []
    other_ids = [cid for cid in other_card_ids if cid != card_id]
    if other_ids:
        combo_notes = find_combination([card_id] + other_ids)
        for note in combo_notes:
            paragraphs.append(note)

    paragraphs.append(advice)

    text = "\n\n".join(paragraphs)

    yes_no_value = None
    if spread_type == "one_card":
        yes_no_value = card["yes_no"][ori]

    return AssembledCard(
        card_id=card_id,
        name_ru=card["name_ru"],
        upright=upright,
        position=position,
        position_label=position_label,
        text=text,
        yes_no=yes_no_value,
    )


def assemble_full_reading(drawn_cards, theme: str, spread_type: str, is_yes_no_question: bool = False):
    """
    drawn_cards: list of app.engine.deck.DrawnCard
    Returns a list of AssembledCard plus a joined full-text reading.
    """
    all_ids = [dc.card_id for dc in drawn_cards]
    assembled = []
    for dc in drawn_cards:
        ac = assemble_card_reading(
            card_id=dc.card_id,
            upright=dc.upright,
            theme=theme,
            spread_type=spread_type,
            position=dc.position,
            other_card_ids=all_ids,
        )
        assembled.append(ac)

    parts = []
    for ac in assembled:
        header = f"{ac.name_ru}" + (f" ({ac.position_label})" if ac.position_label else "")
        header += " — перевёрнутая" if not ac.upright else ""
        parts.append(f"**{header}**\n{ac.text}")
    full_text = "\n\n---\n\n".join(parts)

    yes_no_summary = None
    if spread_type == "one_card" and is_yes_no_question and assembled:
        yes_no_summary = assembled[0].yes_no

    return assembled, full_text, yes_no_summary

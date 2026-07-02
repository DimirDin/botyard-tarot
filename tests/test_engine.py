import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from app.engine.content_loader import all_card_ids, THEMES
from app.engine.template_engine import assemble_card_reading
from app.engine.deck import draw_spread, SPREAD_POSITIONS


def test_78_cards_loaded():
    assert len(all_card_ids()) == 78


@pytest.mark.parametrize("theme", THEMES)
def test_all_cards_all_themes_no_crash(theme):
    for cid in all_card_ids():
        for upright in (True, False):
            ac = assemble_card_reading(cid, upright, theme, "three_card", 1)
            assert ac.text


def test_determinism():
    a = assemble_card_reading("major_16_tower", True, "love", "three_card", 1, ["major_13_death"])
    b = assemble_card_reading("major_16_tower", True, "love", "three_card", 1, ["major_13_death"])
    assert a.text == b.text


@pytest.mark.parametrize("spread_type", list(SPREAD_POSITIONS.keys()))
def test_draw_spread_no_repeats(spread_type):
    drawn = draw_spread(spread_type)
    ids = [d.card_id for d in drawn]
    assert len(ids) == len(set(ids))
    assert len(ids) == SPREAD_POSITIONS[spread_type]


def test_combination_note_spliced_in():
    ac = assemble_card_reading(
        "major_16_tower", True, "general", "three_card", 1, other_card_ids=["major_13_death"]
    )
    assert "Смерть" in ac.text or "обрушится резко" in ac.text

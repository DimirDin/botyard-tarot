#!/usr/bin/env python3
"""
Sanity/verification script for the offline reading engine.

Checks:
1. All 78 cards load without error and have all 6 themes x 2 orientations
   present (wave-2 themes may be TODO stubs, but must not crash / KeyError).
2. Determinism: the same (card, theme, orientation, spread, position) tuple
   always produces byte-identical assembled text.
3. No crashes across all 78 cards x all 6 themes x both orientations x all
   3 spread types x every valid position.
4. Full-spread assembly works for one_card, three_card and celtic_cross,
   including combination-note splicing.

Run: python3 scripts/verify_engine.py
"""
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.engine.content_loader import all_card_ids, THEMES
from app.engine.template_engine import assemble_card_reading, assemble_full_reading
from app.engine.deck import draw_spread, SPREAD_POSITIONS


def check_all_cards_all_themes():
    ids = all_card_ids()
    assert len(ids) == 78, f"Expected 78 cards, got {len(ids)}"
    errors = []
    for cid in ids:
        for theme in THEMES:
            for upright in (True, False):
                for spread_type, n in SPREAD_POSITIONS.items():
                    for pos in range(n):
                        try:
                            assemble_card_reading(cid, upright, theme, spread_type, pos)
                        except Exception as e:
                            errors.append(f"{cid}/{theme}/{upright}/{spread_type}/{pos}: {e}")
    if errors:
        print(f"FAILED: {len(errors)} errors")
        for e in errors[:20]:
            print(" -", e)
        sys.exit(1)
    total = len(ids) * len(THEMES) * 2 * sum(SPREAD_POSITIONS.values())
    print(f"OK: {total} card/theme/orientation/spread/position combos assembled with no crash.")


def check_determinism():
    cid = "major_16_tower"
    a = assemble_card_reading(cid, True, "love", "three_card", 1, other_card_ids=["major_13_death"])
    b = assemble_card_reading(cid, True, "love", "three_card", 1, other_card_ids=["major_13_death"])
    assert a.text == b.text, "Determinism check failed: same input produced different output"
    print("OK: determinism check passed (same input -> identical output).")


def check_full_spreads():
    rng = random.Random(42)
    for spread_type in ("one_card", "three_card", "celtic_cross"):
        drawn = draw_spread(spread_type, rng=rng)
        assembled, full_text, yes_no = assemble_full_reading(
            drawn, theme="general", spread_type=spread_type,
            is_yes_no_question=(spread_type == "one_card"),
        )
        assert len(assembled) == SPREAD_POSITIONS[spread_type]
        assert full_text
        print(f"OK: {spread_type} full assembly produced {len(full_text)} chars, "
              f"{len(assembled)} cards, yes_no={yes_no}")


if __name__ == "__main__":
    check_all_cards_all_themes()
    check_determinism()
    check_full_spreads()
    print("\nAll engine checks passed.")

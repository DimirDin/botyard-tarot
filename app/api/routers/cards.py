from fastapi import APIRouter, HTTPException

from app.engine.content_loader import load_all_cards, get_card, all_card_ids

router = APIRouter(prefix="/api/cards", tags=["cards"])


@router.get("")
async def list_cards():
    cards = load_all_cards()
    return [
        {
            "id": c["id"], "name_ru": c["name_ru"], "name_en": c["name_en"],
            "arcana": c["arcana"], "suit": c["suit"], "image_ref": c["image_ref"],
        }
        for c in cards.values()
    ]


@router.get("/{card_id}")
async def get_card_detail(card_id: str):
    if card_id not in all_card_ids():
        raise HTTPException(404, "Card not found")
    return get_card(card_id)

#!/usr/bin/env python3
"""
Content generator for the AI-Tarot offline database.

This script is the single source of truth for how card content is *authored*.
It embeds real tarot symbolism per card (keywords, core upright/reversed essence,
elemental/numerological flavor) and composes it into distinct, meaningful Russian
text per theme via theme-specific sentence templates.

Wave 1 (COMPLETE for all 78 cards): general, love, career
Wave 2 (COMPLETE for all 78 cards): finance, health, spirit

Run: python3 scripts/generate_content.py
Writes: content/cards/<id>.json (one file per card) + content/cards/_index.json
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "content", "cards")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# CARD DATA
# Each card: id, name_ru, name_en, arcana, suit, number, element, keywords,
#            essence_up, essence_rev  (short core-meaning phrases, hand-written,
#            used as the spine every theme paragraph is built around)
# ---------------------------------------------------------------------------

MAJOR = [
    dict(id="major_00_fool", name_ru="Шут", name_en="The Fool", number=0, element="Воздух",
         keywords=["новое начало", "спонтанность", "риск", "свобода", "наивность"],
         essence_up="лёгкий, почти беспечный шаг в неизвестность — момент, когда доверие к жизни важнее готового плана",
         essence_rev="риск, который перестал быть смелым и стал безрассудным; шаг вслепую там, где нужна пауза"),
    dict(id="major_01_magician", name_ru="Маг", name_en="The Magician", number=1, element="Воздух",
         keywords=["воля", "мастерство", "ресурсы", "действие", "проявление"],
         essence_up="момент, когда все нужные инструменты уже в ваших руках и остаётся только направить волю в одну точку",
         essence_rev="способности есть, но воля рассеяна или используется для манипуляции, а не для создания"),
    dict(id="major_02_high_priestess", name_ru="Верховная Жрица", name_en="The High Priestess", number=2, element="Вода",
         keywords=["интуиция", "тайна", "внутреннее знание", "покой", "подсознание"],
         essence_up="тихое внутреннее знание, которое не нужно доказывать словами — достаточно довериться собственному чутью",
         essence_rev="интуиция заглушена шумом извне, важные сигналы игнорируются или скрываются секреты"),
    dict(id="major_03_empress", name_ru="Императрица", name_en="The Empress", number=3, element="Земля",
         keywords=["изобилие", "забота", "плодородие", "чувственность", "рост"],
         essence_up="щедрое, плодородное время, когда забота о себе и других приносит зримые плоды",
         essence_rev="избыточная забота превращается в зависимость, либо ресурс истощён и заботиться не о ком и нечем"),
    dict(id="major_04_emperor", name_ru="Император", name_en="The Emperor", number=4, element="Огонь",
         keywords=["структура", "власть", "стабильность", "контроль", "порядок"],
         essence_up="твёрдая структура и ясные правила, которые дают опору, а не давят",
         essence_rev="контроль превращается в жёсткость, авторитет используется как давление, а не защита"),
    dict(id="major_05_hierophant", name_ru="Иерофант", name_en="The Hierophant", number=5, element="Земля",
         keywords=["традиция", "наставничество", "система", "убеждения", "обучение"],
         essence_up="проверенный путь, наставник или система правил, которые стоит уважать, а не изобретать заново",
         essence_rev="догма душит живое чувство, правила выполняются формально или наставник оказался не тем"),
    dict(id="major_06_lovers", name_ru="Влюблённые", name_en="The Lovers", number=6, element="Воздух",
         keywords=["выбор", "союз", "гармония", "ценности", "притяжение"],
         essence_up="выбор, сделанный из глубокого согласия с собой, и союз, в котором два целых дополняют друг друга",
         essence_rev="разлад между сердцем и головой, неверный выбор или партнёрство, построенное на компромиссе с собой"),
    dict(id="major_07_chariot", name_ru="Колесница", name_en="The Chariot", number=7, element="Вода",
         keywords=["воля", "движение вперёд", "победа", "дисциплина", "направление"],
         essence_up="собранная воля и чёткое направление позволяют удержать в узде разнонаправленные силы и вырваться вперёд",
         essence_rev="силы тянут в разные стороны, движение теряет управление или превращается в агрессивный напор"),
    dict(id="major_08_strength", name_ru="Сила", name_en="Strength", number=8, element="Огонь",
         keywords=["внутренняя сила", "мягкость", "храбрость", "терпение", "укрощение"],
         essence_up="тихая, но несгибаемая сила, которая укрощает даже самого дикого зверя мягкостью, а не принуждением",
         essence_rev="внутренний зверь берёт верх — импульсивность, сомнение в себе или показная бравада вместо настоящей силы"),
    dict(id="major_09_hermit", name_ru="Отшельник", name_en="The Hermit", number=9, element="Земля",
         keywords=["уединение", "поиск", "мудрость", "самоанализ", "свет внутри"],
         essence_up="сознательный уход от суеты, чтобы услышать собственный внутренний голос и найти свой свет",
         essence_rev="уединение перерастает в изоляцию и одиночество, поиск смысла заходит в тупик"),
    dict(id="major_10_wheel", name_ru="Колесо Фортуны", name_en="Wheel of Fortune", number=10, element="Огонь",
         keywords=["судьба", "цикл", "перемены", "поворот", "удача"],
         essence_up="поворот колеса, который приносит перемены, будто бы случайные, но на деле логично назревшие",
         essence_rev="ощущение, что колесо крутится против вас, полоса неудач или сопротивление неизбежным переменам"),
    dict(id="major_11_justice", name_ru="Справедливость", name_en="Justice", number=11, element="Воздух",
         keywords=["баланс", "истина", "причина и следствие", "решение", "честность"],
         essence_up="ясный, взвешенный итог: то, что было посеяно честно, возвращается по справедливости",
         essence_rev="перекос весов, несправедливое решение или уклонение от ответственности за собственный выбор"),
    dict(id="major_12_hanged_man", name_ru="Повешенный", name_en="The Hanged Man", number=12, element="Вода",
         keywords=["пауза", "новый взгляд", "жертва", "отпускание", "перспектива"],
         essence_up="осознанная пауза и взгляд на ситуацию под непривычным углом дают то понимание, которого не было в спешке",
         essence_rev="бессмысленное застревание, жертва без смысла или упрямый отказ посмотреть на вещи иначе"),
    dict(id="major_13_death", name_ru="Смерть", name_en="Death", number=13, element="Вода",
         keywords=["завершение", "трансформация", "конец цикла", "освобождение", "перерождение"],
         essence_up="честное завершение того, что уже отжило своё, — и место, которое освобождается, обязательно заполнится новым",
         essence_rev="судорожное цепляние за отжившее, страх перемен или затянувшийся, незавершённый переход"),
    dict(id="major_14_temperance", name_ru="Умеренность", name_en="Temperance", number=14, element="Огонь",
         keywords=["баланс", "гармония", "терпение", "смешение", "исцеление"],
         essence_up="терпеливое смешение крайностей в единый гармоничный поток, без спешки и без насилия над собой",
         essence_rev="крайности, которые не желают уравновешиваться, нетерпение или несогласованность между частями жизни"),
    dict(id="major_15_devil", name_ru="Дьявол", name_en="The Devil", number=15, element="Земля",
         keywords=["зависимость", "искушение", "тень", "материальное", "оковы"],
         essence_up="притяжение к тому, что даёт быстрое удовольствие, но постепенно превращается в цепи собственного выбора",
         essence_rev="осознание оков и первый, пока неуверенный шаг к тому, чтобы их снять"),
    dict(id="major_16_tower", name_ru="Башня", name_en="The Tower", number=16, element="Огонь",
         keywords=["внезапный слом", "откровение", "разрушение иллюзий", "кризис", "освобождение"],
         essence_up="резкое обрушение того, что держалось на иллюзии, — болезненно, но именно так расчищается место для настоящего",
         essence_rev="разрушение, которого удалось избежать ценой затягивания неизбежного, или последствия уже случившегося кризиса"),
    dict(id="major_17_star", name_ru="Звезда", name_en="The Star", number=17, element="Воздух",
         keywords=["надежда", "вдохновение", "исцеление", "вера", "ясность"],
         essence_up="тихая надежда после бури — ясность, вдохновение и вера в то, что дальше будет легче",
         essence_rev="надежда истощена, разочарование заслоняет свет, вера в лучшее подорвана усталостью"),
    dict(id="major_18_moon", name_ru="Луна", name_en="The Moon", number=18, element="Вода",
         keywords=["иллюзия", "подсознание", "страх", "неопределённость", "интуиция"],
         essence_up="путь через туман неопределённости, где интуиция важнее логики, а страхи преувеличены полусветом",
         essence_rev="туман начинает рассеиваться, скрытое понемногу выходит на свет, но тревога ещё не до конца отпустила"),
    dict(id="major_19_sun", name_ru="Солнце", name_en="The Sun", number=19, element="Огонь",
         keywords=["радость", "успех", "ясность", "жизненная сила", "открытость"],
         essence_up="ясный, тёплый успех без оговорок — то редкое время, когда всё складывается почти без усилий",
         essence_rev="радость приглушена, успех откладывается или скрыт за излишней скромностью и сомнением"),
    dict(id="major_20_judgement", name_ru="Суд", name_en="Judgement", number=20, element="Огонь",
         keywords=["пробуждение", "призвание", "итог", "прощение", "новый уровень"],
         essence_up="момент пробуждения и честного подведения итогов, после которого начинается качественно новый этап",
         essence_rev="самокритика, которая мешает услышать собственный зов, или отказ признать очевидные итоги"),
    dict(id="major_21_world", name_ru="Мир", name_en="The World", number=21, element="Земля",
         keywords=["завершение", "целостность", "достижение", "интеграция", "полнота цикла"],
         essence_up="полное, гармоничное завершение цикла — всё встало на место, и можно с гордостью выдохнуть",
         essence_rev="цикл почти завершён, но что-то не даёт поставить финальную точку, ощущение незавершённости"),
]

SUITS = {
    "wands": dict(name="Жезлов", element="Огонь", sphere="воля, энергия, страсть, дело и амбиции"),
    "cups": dict(name="Кубков", element="Вода", sphere="чувства, отношения, интуиция и эмоциональная жизнь"),
    "swords": dict(name="Мечей", element="Воздух", sphere="мысли, слова, конфликты и ясность ума"),
    "pentacles": dict(name="Пентаклей", element="Земля", sphere="тело, деньги, работа и материальный мир"),
}

RANKS = [
    ("ace", "Туз", 1, "чистый, ещё не оформленный импульс новой энергии", "упущенная или заблокированная возможность в самом начале"),
    ("02", "Двойка", 2, "выбор или равновесие между двумя силами", "нерешительность, разлад или застой в балансировании"),
    ("03", "Тройка", 3, "первые видимые плоды совместных усилий", "разочарование в результате или разлад в команде"),
    ("04", "Четвёрка", 4, "передышка и укрепление достигнутого", "застой, который выдают за стабильность"),
    ("05", "Пятёрка", 5, "трение, соперничество и испытание на прочность", "истощение от затянувшегося конфликта"),
    ("06", "Шестёрка", 6, "движение к гармонии после пройденного испытания", "рецидив старой проблемы или неравный обмен"),
    ("07", "Семёрка", 7, "оценка сделанного и стратегический выбор дальше", "сомнение, разбросанность или потеря веры в план"),
    ("08", "Восьмёрка", 8, "ускорение и сосредоточенное движение к цели", "ощущение, что руки связаны, а события буксуют"),
    ("09", "Девятка", 9, "почти достигнутый результат ценой накопленной усталости", "истощение и тревога на пороге финала"),
    ("10", "Десятка", 10, "завершённый цикл во всей полноте, хорошей и тяжёлой одновременно", "перегрузка, которая обесценивает достигнутое"),
    ("page", "Паж", 11, "любопытный ученик, который только открывает для себя эту стихию", "незрелость, несобранность или пустые обещания"),
    ("knight", "Рыцарь", 12, "активное, стремительное движение в духе этой стихии", "импульсивность без цели или, наоборот, буксующее рвение"),
    ("queen", "Королева", 13, "зрелое, тёплое владение этой стихией изнутри", "искажённое, холодное или манипулятивное проявление этой энергии"),
    ("king", "Король", 14, "уверенное, мастерское управление этой стихией вовне", "власть, скатившаяся в деспотизм или холодный расчёт"),
]

def build_minor():
    cards = []
    for suit_key, suit in SUITS.items():
        for rank_key, rank_name, number, up, rev in RANKS:
            cid = f"minor_{suit_key}_{rank_key}"
            name_ru = f"{rank_name} {suit['name']}"
            name_en = f"{rank_name} of {suit_key.capitalize()}"
            kw = [suit["sphere"].split(",")[0].strip(), rank_name.lower()]
            cards.append(dict(
                id=cid, name_ru=name_ru, name_en=name_en, number=number,
                suit=suit_key, element=suit["element"],
                keywords=[suit["sphere"], rank_name.lower()],
                essence_up=f"{up} в сфере, где правят {suit['sphere']}",
                essence_rev=f"{rev} в сфере, где правят {suit['sphere']}",
            ))
    return cards

MINOR = build_minor()

for c in MAJOR:
    c["arcana"] = "major"
    c["suit"] = None
for c in MINOR:
    c["arcana"] = "minor"

ALL_CARDS = MAJOR + MINOR
assert len(ALL_CARDS) == 78, len(ALL_CARDS)

# ---------------------------------------------------------------------------
# THEME TEMPLATES (wave 1: general/love/career fully authored for all cards)
# ---------------------------------------------------------------------------

def kw_str(card):
    return ", ".join(card["keywords"])

def general_text(card, up):
    essence = card["essence_up"] if up else card["essence_rev"]
    if up:
        return (f"{card['name_ru']} в прямом положении говорит о том, что в жизнь сейчас входит {essence}. "
                f"Ключевые слова этой карты — {kw_str(card)} — точно описывают энергию момента: она не требует борьбы, "
                f"достаточно позволить событиям идти своим чередом и оставаться внимательным к знакам.")
    else:
        return (f"{card['name_ru']} в перевёрнутом положении указывает на {essence}. "
                f"Обычно светлые качества карты — {kw_str(card)} — сейчас искажены или заблокированы, и это стоит "
                f"признать честно, а не прятать за оправданиями, чтобы ситуация не затянулась дольше необходимого.")

def love_text(card, up):
    essence = card["essence_up"] if up else card["essence_rev"]
    if up:
        return (f"В отношениях {card['name_ru']} прямо означает {essence}. Это время, когда чувства можно проявлять "
                f"открыто: партнёрство (или его поиск) выигрывает от искренности и от готовности видеть в другом "
                f"человеке не проекцию ожиданий, а живого союзника.")
    else:
        return (f"В любовной сфере перевёрнутая {card['name_ru']} предупреждает: {essence}. Стоит присмотреться, "
                f"не подменяются ли настоящая близость привычкой или страхом остаться одному — честный разговор "
                f"важнее красивых слов, которые ничего не меняют.")

def career_text(card, up):
    essence = card["essence_up"] if up else card["essence_rev"]
    if up:
        return (f"В работе и карьере {card['name_ru']} в прямом положении отражает {essence}. Это благоприятный момент "
                f"для того, чтобы делать ставку на собственные сильные стороны и двигаться по выбранному пути "
                f"уверенно, не размениваясь на чужие ожидания.")
    else:
        return (f"На профессиональном поле перевёрнутая {card['name_ru']} сигналит: {essence}. Прежде чем принимать "
                f"важные решения по работе, стоит трезво оценить, где реальный прогресс подменяется видимостью "
                f"занятости или где чужое давление важнее собственных целей.")

def finance_text(card, up):
    essence = card["essence_up"] if up else card["essence_rev"]
    if up:
        return (f"В денежных вопросах {card['name_ru']} говорит о том же, что и в целом: {essence}. Финансовое "
                f"решение, принятое сейчас в духе этой энергии, скорее укрепит, чем ослабит вашу устойчивость.")
    else:
        return (f"В деньгах перевёрнутая {card['name_ru']} предупреждает о том же искажении: {essence}. "
                f"Прежде чем тратить или вкладывать, стоит на время притормозить и свериться с реальными цифрами.")

def health_text(card, up):
    essence = card["essence_up"] if up else card["essence_rev"]
    if up:
        return (f"На уровне тела и энергии {card['name_ru']} отражает {essence}. Самочувствие сейчас во многом "
                f"зависит от того, насколько вы готовы слушать сигналы тела, а не игнорировать их.")
    else:
        return (f"В теме здоровья перевёрнутая {card['name_ru']} указывает на {essence}. Это повод обратить "
                f"больше внимания на профилактику и восстановление, а не откладывать заботу о себе на потом.")

def spirit_text(card, up):
    essence = card["essence_up"] if up else card["essence_rev"]
    if up:
        return (f"В духовном плане {card['name_ru']} говорит о {essence}. Это хорошее время для практик, "
                f"которые укрепляют связь с собственным внутренним компасом.")
    else:
        return (f"На духовном уровне перевёрнутая {card['name_ru']} указывает на {essence}. "
                f"Стоит вернуться к простым практикам заземления, прежде чем искать новые ответы.")

ADVICE_UP_POOL = [
    "Действуйте в согласии с этой энергией, не оглядываясь на сомнения — сейчас она на вашей стороне.",
    "Доверьтесь моменту и сделайте один конкретный шаг уже сегодня.",
    "Позвольте этому качеству проявиться в полную силу — торопить его не нужно.",
    "Используйте этот ресурс сейчас, пока обстоятельства ему благоприятствуют.",
]
ADVICE_REV_POOL = [
    "Не спешите с решением — сначала честно назовите проблему вслух.",
    "Сделайте паузу и вернитесь к этому вопросу, когда эмоции улягутся.",
    "Проверьте, не выдаёте ли вы усталость или страх за окончательный ответ.",
    "Ищите баланс: крайность, в которую вы попали, требует не борьбы, а корректировки курса.",
]

def advice_text(card, up, idx):
    pool = ADVICE_UP_POOL if up else ADVICE_REV_POOL
    return f"Совет: {pool[idx % len(pool)]}"

YES_NO_MAJOR_UP = {
    "major_16_tower": "нет", "major_18_moon": "возможно", "major_12_hanged_man": "возможно",
    "major_15_devil": "нет", "major_13_death": "возможно",
}
YES_NO_MAJOR_REV = {
    "major_19_sun": "возможно", "major_17_star": "возможно", "major_21_world": "возможно",
}

def yes_no(card, up, idx):
    if up:
        if card["id"] in YES_NO_MAJOR_UP:
            return YES_NO_MAJOR_UP[card["id"]]
        return "да" if idx % 3 != 1 else "возможно"
    else:
        if card["id"] in YES_NO_MAJOR_REV:
            return YES_NO_MAJOR_REV[card["id"]]
        return "нет" if idx % 3 != 1 else "возможно"

# Wave 2 (finance/health/spirit): now complete for all 78 cards, generated by the
# same essence-driven templates used for general/love/career.
def build_card_json(card, idx):
    up = True
    down = False
    meanings = {
        "general": {"upright": general_text(card, up), "reversed": general_text(card, down)},
        "love": {"upright": love_text(card, up), "reversed": love_text(card, down)},
        "career": {"upright": career_text(card, up), "reversed": career_text(card, down)},
        "finance": {"upright": finance_text(card, up), "reversed": finance_text(card, down)},
        "health": {"upright": health_text(card, up), "reversed": health_text(card, down)},
        "spirit": {"upright": spirit_text(card, up), "reversed": spirit_text(card, down)},
    }

    return {
        "id": card["id"],
        "name_ru": card["name_ru"],
        "name_en": card["name_en"],
        "arcana": card["arcana"],
        "suit": card["suit"],
        "number": card["number"],
        "element": card["element"],
        "keywords": card["keywords"],
        "image_ref": f"cards/{card['id']}.png",
        "meanings": meanings,
        "yes_no": {"upright": yes_no(card, True, idx), "reversed": yes_no(card, False, idx)},
        "advice": {"upright": advice_text(card, True, idx), "reversed": advice_text(card, False, idx)},
    }

def main():
    index = []
    for i, card in enumerate(ALL_CARDS):
        data = build_card_json(card, i)
        path = os.path.join(OUT_DIR, f"{card['id']}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        index.append({"id": card["id"], "name_ru": card["name_ru"], "arcana": card["arcana"], "suit": card["suit"]})
    with open(os.path.join(OUT_DIR, "_index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"Generated {len(index)} cards into {OUT_DIR}")
    print("Wave 2 (finance/health/spirit): complete for all 78 cards")

if __name__ == "__main__":
    main()

"""Analytics with Timeframe"""
import json
from collections import defaultdict
from datetime import datetime, timedelta

def analyze_shelling_timeframe(timeframe='day'):
    """Analyze shelling for a given timeframe ('day', 'week', 'month')."""
    regions_keywords = {
        "Вінницька": ["вінниц", "вінницьк"],
        "Волинська": ["волин", "луцьк"],
        "Дніпропетровська": ["дніпро", "дніпропетров", "павлоград", "кривий ріг"],
        "Донецька": ["донецьк", "краматорськ", "маріуполь", "бахмут"],
        "Житомирська": ["житомир"],
        "Закарпатська": ["ужгород", "закарпат"],
        "Запорізька": ["запоріж", "запорізьк"],
        "Івано-Франківська": ["івано-франків", "франківськ"],
        "Київська": ["київська"],
        "Кіровоградська": ["кіровоград", "кропивницьк"],
        "Луганська": ["луганськ", "сєвєродонецьк"],
        "Львівська": ["львів", "львівськ"],
        "Миколаївська": ["миколаїв"],
        "Одеська": ["одеса", "одеськ"],
        "Полтавська": ["полтава", "полтавськ"],
        "Рівненська": ["рівне", "рівненськ"],
        "Сумська": ["сум", "сумськ"],
        "Тернопільська": ["терноп", "тернопільськ"],
        "Харківська": ["харків", "харківськ"],
        "Херсонська": ["херсон"],
        "Хмельницька": ["хмельницьк"],
        "Черкаська": ["черкас"],
        "Чернівецька": ["чернівц", "буковин"],
        "Чернігівська": ["чернігів"],
        "Київ": ["київ"],
        "Автономна Республіка Крим": ["крим", "симферополь", "ялта"],
    }

    region_translit = {
        "Вінницька": "Vinnytska",
        "Волинська": "Volynska",
        "Дніпропетровська": "Dnipropetrovska",
        "Донецька": "Donetska",
        "Житомирська": "Zhytomyrska",
        "Закарпатська": "Zakarpatska",
        "Запорізька": "Zaporizka",
        "Івано-Франківська": "Ivano-Frankivska",
        "Київська": "Kyivska",
        "Кіровоградська": "Kirovohradska",
        "Луганська": "Luhanska",
        "Львівська": "Lvivska",
        "Миколаївська": "Mykolaivska",
        "Одеська": "Odeska",
        "Полтавська": "Poltavska",
        "Рівненська": "Rivnenska",
        "Сумська": "Sumska",
        "Тернопільська": "Ternopilska",
        "Харківська": "Kharkivska",
        "Херсонська": "Khersonska",
        "Хмельницька": "Khmelnytska",
        "Черкаська": "Cherkaska",
        "Чернівецька": "Chernivetska",
        "Чернігівська": "Chernihivska",
        "Київ": "Kyiv",
        "Автономна Республіка Крим": "Avtonomna Respublika Krym",
    }

    alert_keywords = ['вибух', 'вибухи', 'удар', 'удари']

    with open('@povitryanatrivogaaa_messages.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    explosions_by_region = defaultdict(int)
    today_str = datetime.now().strftime('%Y-%m-%d')

    if timeframe == 'day':
        start_date = datetime.now().date()
    elif timeframe == 'week':
        start_date = (datetime.now() - timedelta(days=7)).date()
    elif timeframe == 'month':
        start_date = (datetime.now() - timedelta(days=30)).date()
    else:
        raise ValueError("Invalid timeframe. Choose 'day', 'week', or 'month'.")

    for entry in data:
        msg = entry.get("message", "")
        date_str = entry.get("date", "")

        if not msg or not date_str:
            continue

        msg_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').date()

        if msg_date < start_date:
            continue

        msg = msg.lower()

        if any(kw in msg for kw in alert_keywords):
            for region, keys in regions_keywords.items():
                if any(k in msg for k in keys):
                    explosions_by_region[region] += 1
                    break

    result = {}
    for region_ukr, translit in region_translit.items():
        result[translit] = explosions_by_region.get(region_ukr, 0)

    return result

import json
from collections import defaultdict

regions_keywords = {
    "Вінницька": ["вінниц", "вінницьк"],
    "Волинська": ["волин", "луцьк"],
    "Дніпропетровська": ["дніпро", "дніпропетров", "павлоград", "кривий ріг"],
    "Донецька": ["донецьк", "краматорськ", "маріуполь", "бахмут"],
    "Житомирська": ["житомир"],
    "Закарпатська": ["ужгород", "закарпат"],
    "Запорізька": ["запоріж", "запорізьк"],
    "Івано-Франківська": ["івано-франків", "франківськ"],
    "Київська": ["київ", "київська"],
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
}

alert_keywords = ['вибух', 'вибухи', 'удар', 'удари']

with open('@povitryanatrivogaaa_messages.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

explosions_by_region = defaultdict(int)

for entry in data:
    msg = entry.get("message", "")
    if not msg:
        continue

    msg = msg.lower()

    if any(kw in msg for kw in alert_keywords):
        for region, keys in regions_keywords.items():
            if any(k in msg for k in keys):
                explosions_by_region[region] += 1
                break

with open('explosions_by_region.json', 'w', encoding='utf-8') as f_out:
    json.dump(explosions_by_region, f_out, ensure_ascii=False, indent=2)

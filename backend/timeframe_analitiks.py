"""Analytics with Timeframe"""
import json
from collections import defaultdict
from datetime import datetime, timedelta


# def filter_shelling(shelling : list):
import re
from datetime import datetime

data = [{'date': '2025-04-13 21:58:45', 'message': '⚠️✈️**Загрoза БПЛA типу** **"Shahed"**:\n▪️Черкащина→Умань/Вінниччина.\n▪️Кіровоградщина→Черкащина/Вінничина.\n__Напрямок може змінюватися__.\n**Перебувайте в укриттях**!'}, {'date': '2025-04-13 21:48:15', 'message': '💥 Черкaщина - вибухи'}, {'date': '2025-04-13 21:44:20', 'message': '🟢 00:27 Відбій пов. тривоги в \n\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0 Полтавська область\n   n🟢 00:43 Відбій пов. тривоги в \n                 Дніпропетровська область'}, {'date': '2025-04-13 21:27:20', 'message': '⚠️✈️**Загрoза БПЛA типу** **"Shahed"**:\n▪️Черкащина→Шпола  а/Звенигородка\n▪️Кіровоградщина→Черкащина.\n▪️Кіровоградщина→Новоукраїнка/Миколаївщина.\n_ __Напрямок може змінюватися__.\n**Перебувайте в укриттях**!'}, {'date': '2025-04-13 21:17:39', 'message': '🔴 00:17 Повітряна тривога в \n                 Полтавська область\n🔴 00:21 Повітряна тривога в \n                 Звенигородський район\n🔴 00:21 Повітряна тривога в \n                 Уманський район'}, {'date': '2025-04-13 21:12:08', 'message': '⚠️✈️ **Загрoза БПЛA типу** **"Shahed"**:\n▪️Полтавщина→Дніпропетровщина.\n▪️Кіровоградщина→Черк кащина.\n▪️Кіровоградщина→Кропивницький|р\n__Напрямок може змінюватися__.\n**Перебувайте в  укриттях**!'}, {'date': '2025-04-13 21:04:28', 'message': '🔴 00:04 Повітряна тривога в \n                 Черкаський район\n🔴 00:04 Повітряна тривога в \n                 Золотоніський район'}, {'date': '2025-04-13 21:03:35', 'message': '🟢 00:00 Відбій пов. тривоги в \n\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0 Вінницька область\n🟢 00:00 Відбій пов. тривоги в \n\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0 Чернігівська область\n🟢 00:00 Відбій пов. тривоги в \n\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0 Запорізька область\n🟢 00:00 Відбій пов. тривоги в \n\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0 Київська область\n🟢 00:00 Відбій пов. тривоги в \n\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0 Сумська область\n🟢 00:00 Відбій пов. тривоги в \n\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0 Харківська область\n🟢 00:00 Відбій пов. тривоги в \n\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0 Полтавська область\n🟢 00:01 Відбій пов. тривоги в \n\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0 м. Київ\n 🟢 00:03 Відбій пов. тривоги в \n                 Донецька область\n🟢 00:04 Відбій пов. тривоги в \n                 Черкаська область'}, {'date': '2025-04-13 20:56:22', 'message': '✈️ **Кропивницький/р-н - обережно**!'}, {'date': '2025-04-13 20:49:29', 'message': "💥ККраматорськ/Слов'янськ (Донеччина) -\xa0 знову вибyхи"}]

def extract_shelling_info(shelling: list):
    alert_keywords = ['вибух', 'вибухи', 'удар', 'удари', 'загроза', 'ракета', 'дрон', 'shahed', '💥', '🚀', '✈️']

    regions_keywords = {
        "Vinnytska": ["вінниц", "вінницьк"],
        "Volynska": ["волин", "луцьк"],
        "Dnipropetrovska": ["дніпро", "дніпропетров", "павлоград", "кривий ріг"],
        "Donetska": ["донецьк", "краматорськ", "маріуполь", "бахмут", "слов'янськ"],
        "Zhytomyrska": ["житомир"],
        "Zakarpatska": ["ужгород", "закарпат"],
        "Zaporizka": ["запоріж", "запорізьк"],
        "Ivano-Frankivska": ["івано-франків", "франківськ"],
        "Kyivska": ["київська"],
        "Kirovohradska": ["кіровоград", "кропивницьк"],
        "Luhanska": ["луганськ", "сєвєродонецьк"],
        "Lvivska": ["львів", "львівськ"],
        "Mykolaivska": ["миколаїв"],
        "Odeska": ["одеса", "одеськ"],
        "Poltavska": ["полтава", "полтавськ", "кременчук"],
        "Rivnenska": ["рівне", "рівненськ"],
        "Sumska": ["сум", "сумськ"],
        "Ternopilska": ["терноп", "тернопільськ"],
        "Kharkivska": ["харків", "харківськ"],
        "Khersonska": ["херсон"],
        "Khmelnytska": ["хмельницьк"],
        "Cherkaska": ["черкас", "золотоноша", "черкащин"],
        "Chernivetska": ["чернівц", "буковин"],
        "Chernihivska": ["чернігів"],
        "Kyiv": ["м. київ", "київ"],
        "Avtonomna Respublika Krym": ["крим", "симферополь", "ялта"],
    }

    result = []
    last_datetime = None

    for entry in shelling:
        msg = entry.get('message', '').lower()
        date_str = entry.get('date', '')
        if not msg or not date_str:
            continue

        try:
            dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except:
            continue

        if last_datetime is None or dt > last_datetime:
            last_datetime = dt

        date = dt.strftime('%Y-%m-%d')
        # Спробуємо витягнути час із повідомлення (якщо є)
        times = re.findall(r'\b\d{2}:\d{2}\b', msg)
        time_used = times[0] if times else dt.strftime('%H:%M')

        if any(keyword in msg for keyword in alert_keywords):
            for region, keywords in regions_keywords.items():
                if any(k in msg for k in keywords):
                    result.append({
                        "date": date,
                        "time": time_used,
                        "city": region
                    })

    last_update_text = last_datetime.strftime('%Y-%m-%d %H:%M') if last_datetime else "🕒 Немає оновлень"

    return result, last_update_text


# def analyze_shelling_timeframe(timeframe='month'):
#     """Analyze shelling for a given timeframe ('day', 'week', 'month')."""
   

#     regions_keywords = {
#         "Вінницька": ["вінниц", "вінницьк"],
#         "Волинська": ["волин", "луцьк"],
#         "Дніпропетровська": ["дніпро", "дніпропетров", "павлоград", "кривий ріг"],
#         "Донецька": ["донецьк", "краматорськ", "маріуполь", "бахмут"],
#         "Житомирська": ["житомир"],
#         "Закарпатська": ["ужгород", "закарпат"],
#         "Запорізька": ["запоріж", "запорізьк"],
#         "Івано-Франківська": ["івано-франків", "франківськ"],
#         "Київська": ["київська"],
#         "Кіровоградська": ["кіровоград", "кропивницьк"],
#         "Луганська": ["луганськ", "сєвєродонецьк"],
#         "Львівська": ["львів", "львівськ"],
#         "Миколаївська": ["миколаїв"],
#         "Одеська": ["одеса", "одеськ"],
#         "Полтавська": ["полтава", "полтавськ"],
#         "Рівненська": ["рівне", "рівненськ"],
#         "Сумська": ["сум", "сумськ"],
#         "Тернопільська": ["терноп", "тернопільськ"],
#         "Харківська": ["харків", "харківськ"],
#         "Херсонська": ["херсон"],
#         "Хмельницька": ["хмельницьк"],
#         "Черкаська": ["черкас"],
#         "Чернівецька": ["чернівц", "буковин"],
#         "Чернігівська": ["чернігів"],
#         "Київ": ["київ"],
#         "Автономна Республіка Крим": ["крим", "симферополь", "ялта"],
#     }
#     region_translit = {
#         "Вінницька": "Vinnytska",
#         "Волинська": "Volynska",
#         "Дніпропетровська": "Dnipropetrovska",
#         "Донецька": "Donetska",
#         "Житомирська": "Zhytomyrska",
#         "Закарпатська": "Zakarpatska",
#         "Запорізька": "Zaporizka",
#         "Івано-Франківська": "Ivano-Frankivska",
#         "Київська": "Kyivska",
#         "Кіровоградська": "Kirovohradska",
#         "Луганська": "Luhanska",
#         "Львівська": "Lvivska",
#         "Миколаївська": "Mykolaivska",
#         "Одеська": "Odeska",
#         "Полтавська": "Poltavska",
#         "Рівненська": "Rivnenska",
#         "Сумська": "Sumska",
#         "Тернопільська": "Ternopilska",
#         "Харківська": "Kharkivska",
#         "Херсонська": "Khersonska",
#         "Хмельницька": "Khmelnytska",
#         "Черкаська": "Cherkaska",
#         "Чернівецька": "Chernivetska",
#         "Чернігівська": "Chernihivska",
#         "Київ": "Kyiv",
#         "Автономна Республіка Крим": "Avtonomna Respublika Krym",
#     }

#     alert_keywords = ['вибух', 'вибухи', 'удар', 'удари']

#     with open('@povitryanatrivogaaa_messages.json', 'r', encoding='utf-8') as f:
#         data = json.load(f)

#     explosions_by_region = defaultdict(int)
#     today_str = datetime.now().strftime('%Y-%m-%d')

#     if timeframe == 'day':
#         start_date = datetime.now().date()
#     elif timeframe == 'week':
#         start_date = (datetime.now() - timedelta(days=7)).date()
#     elif timeframe == 'month':
#         start_date = (datetime.now() - timedelta(days=30)).date()
#     else:
#         raise ValueError("Invalid timeframe. Choose 'day', 'week', or 'month'.")

#     for entry in data:
#         msg = entry.get("message", "")
#         date_str = entry.get("date", "")

#         if not msg or not date_str:
#             continue

#         msg_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').date()

#         if msg_date < start_date:
#             continue

#         msg = msg.lower()

#         if any(kw in msg for kw in alert_keywords):
#             for region, keys in regions_keywords.items():
#                 if any(k in msg for k in keys):
#                     explosions_by_region[region] += 1
#                     break

#     result = {}
#     for region_ukr, translit in region_translit.items():
#         result[translit] = explosions_by_region.get(region_ukr, 0)

#     return result

import schedule
import time
from telethon.sync import TelegramClient
import json


api_id = "25663089"
api_hash = "fc972277aa436080fedcbf8f669df79f"
json_file_path = "backend\\news.json"
js_file_path = "backend\\news.js"
region_channels = {
    "Київ": "@kyivoda",
    "Львів": "@people_of_action",
    "Одеса": "@odeskaODA",
    "Дніпро": "@dnipropetrovskaODA",
    "Харків": "@kharkivoda",
    "Запоріжжя": "@zoda_gov_ua",
    "Черкаси": "@cherkaskaODA",
    "Полтава": "@poltavskaOVA",
    "Вінниця": "@vinnytskaODA",
    "Житомир": "@zhytomyrskaODA",
    "Суми": "@Zhyvytskyy",
    "Чернігів": "@chernigivskaODA",
    "Хмельницький": "@khmelnytskaODA",
    "Івано-Франківськ": "@onyshchuksvitlana",
    "Тернопіль": "@ternopilskaODA",
    "Рівне": "@ODA_RV",
    "Кропивницький": "@kirovogradskaODA",
    "Миколаїв": "@mykolaivskaODA",
    "Луцьк": "@volynskaODA",
    "Херсон": "@khersonskaODA",
    "Чернівці": "@chernivetskaODA",
    "Ужгород": "@zoda_inform",
    "Луганськ": "@luhanskaVTSA",
    "Донецьк": "@DonetskaODA"
}
EXCLUDED_WORDS = ["тривога", "відбій", "мовчання"]

def contains_excluded_words(text):
    lower_text = text.lower()
    return any(word in lower_text for word in EXCLUDED_WORDS)

def get_news():
    with TelegramClient("session_name", api_id, api_hash) as client: 
        news_by_region = {region: [] for region in region_channels}
        last_update = time.strftime("%Y-%m-%d %H:%M:%S")

        for region, channel in region_channels.items():
            messages = client.get_messages(channel, limit=40)
            filtered_news = [
                {"date": msg.date.strftime("%Y-%m-%d %H:%M:%S"), "text": msg.text}
                for msg in messages if msg.text and not contains_excluded_words(msg.text)
            ]
            news_by_region[region] = filtered_news[:3]

        data_to_save = {
            "last_update": last_update,
            "news": news_by_region
        }

        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(data_to_save, json_file, ensure_ascii=False, indent=4)

        with open(js_file_path, "w", encoding="utf-8") as js_file:
            js_file.write("export const data = "+str(data_to_save))


schedule.every(4).seconds.do(get_news)

while True:
    schedule.run_pending()
    time.sleep(4)
import os
import json
import time
from alerts_in_ua import Client as AlertsClient


def get_active_alerts():
    """Get active alerts."""
    
    file_path = 'active_alerts.json'
    if not os.path.exists(file_path):
        file_path = os.path.join('backend', 'active_alerts.json')


    alerts_client = AlertsClient(token="26ffd55f74e65381554687b9410060cf138e00d4ab2203")

    alarm_data = {
        "Vinnytska": "notalarm",
        "Volynska": "notalarm",
        "Dnipropetrovska": "notalarm",
        "Donetska": "notalarm",
        "Zhytomyrska": "notalarm",
        "Zakarpatska": "notalarm",
        "Zaporizka": "notalarm",
        "Ivano-Frankivska": "notalarm",
        "Kyivska": "notalarm",
        "Kirovohradska": "notalarm",
        "Luhanska": "notalarm",
        "Lvivska": "notalarm",
        "Mykolaivska": "notalarm",
        "Odeska": "notalarm",
        "Poltavska": "notalarm",
        "Rivnenska": "notalarm",
        "Sumska": "notalarm",
        "Ternopilska": "notalarm",
        "Kharkivska": "notalarm",
        "Khersonska": "notalarm",
        "Khmelnytska": "notalarm",
        "Cherkaska": "notalarm",
        "Chernihivska": "notalarm",
        "Chernivetska": "notalarm",
        "Kyiv": "notalarm",
        "Avtonomna Respublika Krym": "notalarm"
    }

    translate = {
        "Вінницька область": "Vinnytska",
        "Волинська область": "Volynska",
        "Дніпропетровська область": "Dnipropetrovska",
        "Донецька область": "Donetska",
        "Житомирська область": "Zhytomyrska",
        "Закарпатська область": "Zakarpatska",
        "Запорізька область": "Zaporizka",
        "Івано-Франківська область": "Ivano-Frankivska",
        "Київська область": "Kyivska",
        "Кіровоградська область": "Kirovohradska",
        "Луганська область": "Luhanska",
        "Львівська область": "Lvivska",
        "Миколаївська область": "Mykolaivska",
        "Одеська область": "Odeska",
        "Полтавська область": "Poltavska",
        "Рівненська область": "Rivnenska",
        "Сумська область": "Sumska",
        "Тернопільська область": "Ternopilska",
        "Харківська область": "Kharkivska",
        "Херсонська область": "Khersonska",
        "Хмельницька область": "Khmelnytska",
        "Черкаська область": "Cherkaska",
        "Чернігівська область": "Chernihivska",
        "Чернівецька область": "Chernivetska",
        "Київ": "Kyiv",
        "Автономна Республіка Крим": "Avtonomna Respublika Krym"
    }

    prev_alarm_location_set = set()

    # while True:
    active_alerts = alerts_client.get_active_alerts()

    alarm_location_set = set()

    for alert in active_alerts:
        alarm_location_set.add(translate[alert.location_oblast])

    new_alarm_locations = alarm_location_set - prev_alarm_location_set
    new_cancelation_locations = prev_alarm_location_set - alarm_location_set

    prev_alarm_location_set = alarm_location_set

    for new_alarm_location in new_alarm_locations:
        alarm_data[new_alarm_location] = 'alarm'

    for new_cancelation_location in new_cancelation_locations:
        alarm_data[new_cancelation_location] = 'notalarm'
    return alarm_data
        # with open(file_path, 'w', encoding='utf-8') as json_file:
        #     json.dump(alarm_data, json_file, ensure_ascii=False, indent=4)

        # print("Дані оновлено в 'active_alerts.json'")

# alerts_service.py

import os
from alerts_in_ua import Client as AlertsClient

ALERTS_CLIENT = AlertsClient(token="26ffd55f74e65381554687b9410060cf138e00d4ab2203")

TRANSLATE_LOCATION = {
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
    "м. Київ": "Kyiv",
    "Автономна Республіка Крим": "Avtonomna Respublika Krym"
}

TRANSLATE_ALERTS = {
    "no_alert": "notalarm",
    "active": "alarm",
    "partly": "alarm"
}

DEFAULT_STATE = {eng_name: "notalarm" for eng_name in TRANSLATE_LOCATION.values()}


def get_active_alerts():
    """Fetch current alert status for all oblasts."""
    alarm_data = DEFAULT_STATE.copy()
    alert_locations = ALERTS_CLIENT.get_air_raid_alert_statuses_by_oblast()

    for alert_location in alert_locations:
        alert, location = str(alert_location).split(':')
        alert = TRANSLATE_ALERTS.get(alert)
        location = TRANSLATE_LOCATION.get(location)
        if location and alert:
            alarm_data[location] = alert

    return alarm_data

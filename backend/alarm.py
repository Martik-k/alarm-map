import os
import json
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

    translate_location = {
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
    
    translate_alerts = {"no_alert": "notalarm",
                        "active": "alarm", 
                        "partly": "alarm"}

    alert_locations = alerts_client.get_air_raid_alert_statuses_by_oblast()

    for alert_location in alert_locations:
        alert, location = str(alert_location).split(':')
        alert = translate_alerts[alert]
        location = translate_location.get(location, None)
        if location and alarm_data[location] != alert:
            alarm_data[location] = alert

    return alarm_data   # goes to app.py

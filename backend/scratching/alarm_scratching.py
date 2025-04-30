import os
from alerts_in_ua import Client as AlertsClient
from app.const import TRANSLATE_LOCATION

TRANSLATE_ALARMS = {"no_alert": "notalarm",
                    "active": "alarm", 
                    "partly": "alarm"}

def get_active_alerts():
    """
    Fetches the current active air raid alerts for all regions of Ukraine using an external API.

    It initializes a dictionary with all regions set to 'notalarm' and then updates the status
    for regions where an alert is active based on the API response.

    Returns:
        dict[str, str]: A dictionary where keys are the application's standard location names
                       and values are the corresponding alarm status ('alarm' or 'notalarm').
    """

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

    alert_locations = alerts_client.get_air_raid_alert_statuses_by_oblast()

    for alert_location in alert_locations:
        alert, location = str(alert_location).split(':')
        alert = TRANSLATE_ALARMS[alert]
        location = TRANSLATE_LOCATION.get(location, None)
        if location and alarm_data[location] != alert:
            alarm_data[location] = alert

    return alarm_data

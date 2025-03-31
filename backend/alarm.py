import json
import time
from alerts_in_ua import Client as AlertsClient

alerts_client = AlertsClient(token="26ffd55f74e65381554687b9410060cf138e00d4ab2203")

while True:
    active_alerts = alerts_client.get_active_alerts()

    data = {
        "alerts": []
    }

    for alert in active_alerts:
        data["alerts"].append({
            "id": alert.id,  
            "start": alert.started_at.isoformat() if alert.started_at else None,
            "finish": alert.finished_at.isoformat() if alert.finished_at else None,
            "type": alert.alert_type,
            "location": alert.location_title,
            "location_type": alert.location_type,
            "details": alert.notes
        })

    with open('active_alerts.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print("Дані оновлено в 'active_alerts.json'")

    time.sleep(30)

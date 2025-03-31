"""History of alarm."""
import json
import time
from alerts_in_ua import Client as AlertsClient

FIRST_TOKEN = "faaab9c185f492913ef2f4e455f4b51321d05266ab2203"
SECOND_TOKEN = "26ffd55f74e65381554687b9410060cf138e00d4ab2203"

first_batch = [i for i in range(3, 16) if i not in (6, 7)]
second_batch = [i for i in range(16, 32)]

def fetch_and_save(region_ids, token, file_mode):
    """Scratch the history of alarm and write it in json file."""
    alerts_client = AlertsClient(token=token)
    data = {}

    for region_id in region_ids:
        try:
            active_alerts = alerts_client.get_alerts_history(region_id, period="month_ago")
            data[region_id] = []

            for alert in active_alerts:
                data[region_id].append({
                    "id": alert.id,  
                    "start": alert.started_at.isoformat() if alert.started_at else None,
                    "finish": alert.finished_at.isoformat() if alert.finished_at else None,
                    "type": alert.alert_type,
                    "location": alert.location_title,
                    "location_type": alert.location_type,
                    "details": alert.notes
                })

            print(f"Дані для регіону {region_id} отримано")

        except Exception as e:
            print(f"Помилка отримання даних для регіону {region_id}: {e}")
            data[region_id] = None

        time.sleep(5)
    with open('history_alerts.json', file_mode, encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

fetch_and_save(first_batch, FIRST_TOKEN, 'w')

print("Перший запис завершено. Чекаємо 30 секунд...")
time.sleep(30)

fetch_and_save(second_batch, SECOND_TOKEN, 'a')

print("Дані повністю збережено в 'history_alerts.json'")

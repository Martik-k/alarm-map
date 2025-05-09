"""History of alarm."""
import time
from alerts_in_ua import Client as AlertsClient
import os
from dotenv import load_dotenv
from app.const import TRANSLATE_LOCATION

load_dotenv()
FIRST_TOKEN = os.getenv("FIRST_API_TOKEN")
SECOND_TOKEN = os.getenv("SECOND_API_TOKEN")
THIRD_TOKEN = os.getenv("THIRD_API_TOKEN")
FORTH_TOKEN = os.getenv("FORTH_API_TOKEN")

LOCATIONS = ["Vinnytska", "Volynska", "Dnipropetrovska", "Donetska", "Zhytomyrska", "Zakarpatska", 
             "Zaporizka", "Ivano-Frankivska", "Kyivska", "Kirovohradska", "Luhanska", 
             "Lvivska", "Mykolaivska", "Odeska", "Poltavska", "Rivnenska", "Sumska", 
             "Ternopilska", "Kharkivska", "Khersonska", "Khmelnytska", "Cherkaska", 
             "Chernihivska", "Chernivetska", "Kyiv", "Avtonomna Respublika Krym"]


def fetch_and_save(region_ids, token):
    """
    Fetches the history of air raid alerts for a given 
    list of region IDs using the provided API token.

    It retrieves the alert history for the past month for each region ID and extracts 
    relevant information such as start time, finish time, location title, and whether 
    the alert has finished.
    Error handling is included to catch potential exceptions during data retrieval for a region.
    A delay of 5 seconds is introduced after attempting to fetch data for each region.

    Args:
        region_ids (list[int]): A list of integer IDs representing the regions 
        for which to fetch alert history.
                                 These IDs are specific to the external API.
        token (str): The API token to use for authentication.

    Returns:
        list[list[any]]: A list of lists, where each inner list represents an alert event 
        and contains:
                         - started_at (datetime or None): The start time of the alert.
                         - finished_at (datetime or None): The finish time of the alert.
                         - location_title (str): The title of the location where the alert occurred.
                         - is_finished (bool or None): True if the alert has finished, None 
                         otherwise.
                         Returns an empty list if no data is fetched or an error occurs for 
                         all regions.
    """
    alerts_client = AlertsClient(token=token)
    data = []

    for region_id in region_ids:
        try:
            active_alerts = alerts_client.get_alerts_history(region_id, period="month_ago")
            for alert in active_alerts:
                if alert.location_type == 'oblast':
                    data.append([alert.started_at if alert.started_at else None,
                            alert.finished_at if alert.finished_at else None,
                            TRANSLATE_LOCATION[alert.location_title],
                            False if alert.finished_at else True])

            print(f"Дані для регіону {region_id} отримано")

        except Exception as e:
            print(f"Помилка отримання даних для регіону {region_id}: {e}")

        time.sleep(5)
    return data


def get_month_alerts():
    """
    Fetches the air raid alert history for a predefined set of region ID 
    batches using different API tokens.

    It divides the region IDs into two batches and calls the `fetch_and_save` 
    function for each batch with a specific API token. A 30-second delay is 
    introduced between fetching the two batches.

    Returns:
        list[list[any]]: A combined list of alert history data fetched 
        from both batches of region IDs.
        The structure of each inner list is the same as described in the 
        `fetch_and_save` function.
    """
    first_batch = [i for i in range(3, 16) if i not in (6, 7)]
    second_batch = [i for i in range(16, 32)]
    result_data = []
    result_data += fetch_and_save(first_batch, SECOND_TOKEN)

    print("Перший запис завершено. Чекаємо 30 секунд...")
    time.sleep(30)

    result_data += fetch_and_save(second_batch, THIRD_TOKEN)

    print("Дані повністю збережено")
    return result_data

import json
from datetime import datetime
import matplotlib.pyplot as plt

def calculate_average_duration(region: str, month: int, year: int, file_path: str) -> str:
    """
    Calculates the average duration of alerts in a given region, month, and year.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    total_duration = 0
    alert_count = 0
    for _, alerts in data.items():
        for alert in alerts:
            if alert.get('location') == region:
                alert_start = alert.get('start')
                start_date = datetime.fromisoformat(alert_start)
                if start_date.month == month and start_date.year == year:
                    start_time = datetime.fromisoformat(alert.get('start'))
                    end_time = datetime.fromisoformat(alert.get('finish'))
                    duration = (end_time - start_time).total_seconds()
                    total_duration += duration
                    alert_count += 1
    if alert_count > 0:
        average_duration = total_duration / alert_count
        average_duration_minutes = average_duration / 60
        if average_duration_minutes >= 60:
            average_duration_hours = average_duration_minutes // 60
            average_duration_remainder_minutes = average_duration_minutes % 60
            return f"{int(average_duration_hours)} год {int(average_duration_remainder_minutes)} хв"
        else:
            return f"{average_duration_minutes:.2f} хв"
    else:
        return "Не знайдено тривог для цієї області"

def count_alerts(region: str, month: int, year: int, file_path: str) -> int:
    """
    Counts the number of alerts in a given region, month, and year.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    alert_count = 0
    for _, alerts in data.items():
        for alert in alerts:
            if alert.get('location') == region:
                alert_start = alert.get('start')
                start_date = datetime.fromisoformat(alert_start)

                if start_date.month == month and start_date.year == year:
                    alert_count += 1
    return alert_count

def calculate_alert_percentage(region: str, month: int, year: int, file_path: str) -> float:
    """
    Calculates the percentage of time the alerts were active within 
    the given month in a specific region.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    total_minutes_in_month = 0
    total_alert_minutes = 0
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    total_minutes_in_month = (end_date - start_date).total_seconds() / 60  # в хвилинах
    for _, alerts in data.items():
        for alert in alerts:
            if alert.get('location') == region:
                alert_start = alert.get('start')
                alert_finish = alert.get('finish')
                start_datetime = datetime.fromisoformat(alert_start).replace(tzinfo=None)
                finish_datetime = datetime.fromisoformat(alert_finish).replace(tzinfo=None)
                if start_datetime >= start_date and finish_datetime < end_date:
                    alert_duration = (finish_datetime - start_datetime).total_seconds() / 60
                    total_alert_minutes += alert_duration
    if total_minutes_in_month > 0:
        alert_percentage = (total_alert_minutes / total_minutes_in_month) * 100
    else:
        alert_percentage = 0
    return alert_percentage

def get_last_alert_time(region: str, file_path: str) -> str:
    """
    Returns the start and finish time of the last alert in the given region.
    """
    ukr_months = [
        'січня', 'лютого', 'березня', 'квітня', 'травня', 'червня',
        'липня', 'серпня', 'вересня', 'жовтня', 'листопада', 'грудня'
    ]
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    last_alert_start = None
    last_alert_finish = None
    last_alert_date = None
    for _, alerts in data.items():
        for alert in alerts:
            if alert.get('location') == region:
                alert_start = alert.get('start')
                alert_finish = alert.get('finish')
                start_datetime = datetime.fromisoformat(alert_start).replace(tzinfo=None)
                finish_datetime = datetime.fromisoformat(alert_finish).replace(tzinfo=None)
                if last_alert_start is None or start_datetime > last_alert_start:
                    last_alert_start = start_datetime
                    last_alert_finish = finish_datetime
                    last_alert_date = start_datetime
    if last_alert_start:
        start_time = last_alert_start.strftime('%H:%M')
        finish_time = last_alert_finish.strftime('%H:%M')
        month_index = last_alert_date.month - 1
        formatted_date = f"{last_alert_date.day} {ukr_months[month_index]}"
        return f"{start_time} - {finish_time}, {formatted_date}"
    else:
        return "Тривоги не знайдено"

def plot_alert_durations(region: str, month: int, year: int, file_path: str):
    """
    Plots a bar chart showing the duration of alerts per day for a given month in a specific region.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    days_duration = {day: 0 for day in range(1, 32)}
    for _, alerts in data.items():
        for alert in alerts:
            if alert.get('location') == region:
                alert_start = alert.get('start')
                alert_finish = alert.get('finish')
                start_datetime = datetime.fromisoformat(alert_start).replace(tzinfo=None)
                finish_datetime = datetime.fromisoformat(alert_finish).replace(tzinfo=None)
                if start_datetime.month == month and start_datetime.year == year:
                    day_of_alert = start_datetime.day
                    duration = (finish_datetime - start_datetime).total_seconds() / 3600
                    days_duration[day_of_alert] += duration
    days = [day for day in range(1, 32) if days_duration[day] > 0]
    durations = [days_duration[day] for day in days]
    plt.figure(figsize=(10, 6))
    plt.bar(days, durations, color='#a94442')
    plt.title('Тривалість тривог по днях місяця', fontsize=12)
    plt.xlabel('День місяця', fontsize=10)
    plt.ylabel('Тривалість (години)', fontsize=10)
    plt.xticks(range(1, 32), fontsize=8)
    plt.yticks(fontsize=8)
    plt.grid(axis='y', alpha=0.3, linewidth=0.5)
    plt.tight_layout()
    plt.show()

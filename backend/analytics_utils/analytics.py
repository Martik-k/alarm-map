"""
Analytics.
"""

import base64
from io import BytesIO
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib
matplotlib.use('Agg')

def get_kyiv_time():
    now_kyiv = datetime.now(ZoneInfo("Europe/Kyiv"))
    return now_kyiv.replace(tzinfo=None)

def get_range_bounds(range_prop: str):
    """
    Calculates the start and end datetime objects for a given time range.

    Args:
        range_prop (str): The time range property ('week', 'month', or 'year').

    Returns:
        tuple[datetime, datetime]: A tuple containing the start and end datetime objects.

    Raises:
        ValueError: If an invalid range_prop is provided.
    """
    end = get_kyiv_time()
    if range_prop == "week":
        start = end - timedelta(weeks=1)
    elif range_prop == "month":
        start = end - timedelta(days=30)
    elif range_prop == "year":
        start = end - timedelta(days=365)
    else:
        raise ValueError("Invalid range_prop. Expected: 'week', 'month', or 'year'.")
    return start, end


def calculate_average_duration(lst_region) -> str:
    """
    Calculates the average duration of alerts for a given region.

    Args:
        lst_region (list): A list containing alert count and total duration (timedelta).
                           Expected format: [alert_count (int), total_duration (timedelta), ...].

    Returns:
        str: A human-readable string representing the average duration (e.g., "1 год 30 хв").
             Returns "No alerts found for this region" if alert_count is 0.
    """
    alert_count = lst_region[0]
    total_duration = lst_region[1]

    if alert_count == 0:
        return "No alerts found for this region"

    avg_duration = total_duration / len(lst_region[3])
    total_minutes = int(avg_duration.total_seconds() / 60)

    days = total_minutes // (24 * 60)
    hours = (total_minutes % (24 * 60)) // 60
    minutes = total_minutes % 60

    result = []
    if days > 0:
        result.append(f"{days} дн")
    if hours > 0:
        result.append(f"{hours} год")
    if minutes > 0 or not result:
        result.append(f"{minutes} хв")

    return " ".join(result)



def count_alerts(lst_region) -> int:
    """
    Counts the number of alerts for a given region.

    Args:
        lst_region (list): A list containing alert count.
                           Expected format: [alert_count (int), ...].

    Returns:
        int: The number of alerts.
    """
    
    return lst_region[0]

def calculate_alert_percentage(range_prop: str,  lst_region: dict, start_alarms, start_dictionary) -> float:
    """
    Calculates the percentage of time an alert was active within a given range.

    Args:
        range_prop (str): The time range property ('week', 'month', or 'year').
        lst_region (dict): A dictionary containing alert information, including total duration (timedelta).
                           Expected format: [..., total_duration (timedelta), ...].
        start_alarms (datetime, optional): The overall start time of the alarm system.
                                           Defaults to None.

    Returns:
        float: The percentage of time an alert was active (0.0 to 100.0).
    """
    start = start_dictionary[range_prop]
    end = get_kyiv_time()
    end = end.replace(hour=0 ,minute=0, second=0)
    start = max(start, start_alarms) if start_alarms else start
    total_seconds = (end - start).total_seconds()

    period_starts = lst_region[3]
    alert_seconds = timedelta(0)
    for period_start, delta in period_starts.items():
        if period_start > start_alarms:
            alert_seconds += delta
    alert_seconds = alert_seconds.total_seconds()

    return (alert_seconds / total_seconds) * 100 if total_seconds > 0 else 0


def get_last_alert_time(lst_region) -> str:
    """
    Retrieves the timestamp of the last alert for a given region.

    Args:
        lst_region (list): A list containing the last alert time (datetime).
                           Expected format: [..., ..., last_alert_time (datetime)].

    Returns:
        datetime: The datetime object representing the last alert time.
    """
    return lst_region[2]


TRANSLATE_LOCATION = {
    "Vinnytska": "Вінницька область",
    "Volynska": "Волинська область",
    "Dnipropetrovska": "Дніпропетровська область",
    "Donetska": "Донецька область",
    "Zhytomyrska": "Житомирська область",
    "Zakarpatska": "Закарпатська область",
    "Zaporizka": "Запорізька область",
    "Ivano-Frankivska": "Івано-Франківська область",
    "Kyivska": "Київська область",
    "Kirovohradska": "Кіровоградська область",
    "Luhanska": "Луганська область",
    "Lvivska": "Львівська область",
    "Mykolaivska": "Миколаївська область",
    "Odeska": "Одеська область",
    "Poltavska": "Полтавська область",
    "Rivnenska": "Рівненська область",
    "Sumska": "Сумська область",
    "Ternopilska": "Тернопільська область",
    "Kharkivska": "Харківська область",
    "Khersonska": "Херсонська область",
    "Khmelnytska": "Хмельницька область",
    "Cherkaska": "Черкаська область",
    "Chernihivska": "Чернігівська область",
    "Chernivetska": "Чернівецька область",
    "Kyiv": "м. Київ",
    "Avtonomna Respublika Krym": "Автономна Республіка Крим"
}

def plot_analytics_from_dict(analytics_dict, range_prop, region, last_date):
   
    ukr_months_short = [
        'Січ', 'Лют', 'Бер', 'Кві', 'Тра', 'Чер',
        'Лип', 'Сер', 'Вер', 'Жов', 'Лис', 'Гру'
    ]

    if range_prop not in analytics_dict or region not in analytics_dict[range_prop]:
        print(f"No data for {region} in range {range_prop}")
        return ""

    count, total_duration, latest_end, durations_dict = analytics_dict[range_prop][region]

    if not durations_dict:
        print(f"No alert durations to plot for {region} in {range_prop}")
        return ""

    sorted_keys = sorted(durations_dict.keys())
    durations = [durations_dict[k].total_seconds() / 3600 for k in sorted_keys]
    is_outdated = [k < last_date for k in sorted_keys]

    fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)
    region_ukr = TRANSLATE_LOCATION.get(region, region)
    title = f'Сумарна тривалість тривог (год) - {region_ukr}'
    x_label = 'Дата'
    y_label = 'Тривалість (години)'
    label_format = "%d.%m"
    locator = mticker.AutoLocator()
    rotation = 90

    if range_prop == "year":
        labels = [ukr_months_short[k.month - 1] for k in sorted_keys]
        title += f'\nЗа місяцями, {last_date.year} рік'
        x_label = 'Місяць'
        locator = mticker.MultipleLocator(1)
        rotation = 0
    elif range_prop == "month":
        labels = [k.strftime(label_format) for k in sorted_keys]
        title += f'\nПо днях, {ukr_months_short[last_date.month - 1].lower()} {last_date.year}'
        locator = mticker.MultipleLocator(2 if len(sorted_keys) > 15 else 1)
    elif range_prop == "week":
        labels = [k.strftime(label_format) for k in sorted_keys]
        title += f'\nПо днях, тиждень до {last_date.strftime(label_format)}'
    else:
        print(f"Unsupported range_prop: {range_prop}")
        return ""

    x_positions = range(len(labels))

    for i, (v, outdated) in enumerate(zip(durations, is_outdated)):
        color = '#cccccc' if outdated else '#a94442'
        ax.bar(i, v, color=color)
        if outdated:
            ax.text(i, v + 0.05, 'нема даних', ha='center', va='bottom', fontsize=7, rotation=90, color='gray')

    for i, (v, outdated) in enumerate(zip(durations, is_outdated)):
        if v > 0 and not outdated:
            label_text = f"{v:.1f}" if v % 1 != 0 else f"{int(v)}"
            ax.text(i, v + 0.05, label_text, ha='center', va='bottom', fontsize=8, rotation=90)

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(labels, rotation=rotation, ha='center')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.xaxis.set_major_locator(locator)

    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=90)
    plt.close(fig)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

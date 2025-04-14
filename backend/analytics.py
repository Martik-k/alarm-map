import base64
from io import BytesIO
import json
from datetime import datetime, timedelta
import calendar
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def shift_date_by_months(date: datetime, months: int) -> datetime:
    month = date.month - 1 + months
    year = date.year + month // 12
    month = month % 12 + 1
    day = min(date.day, calendar.monthrange(year, month)[1])
    return date.replace(year=year, month=month, day=day)

def get_range_bounds(range_prop: str, shift_months: int = 0) -> tuple[datetime, datetime]:
    """
    Returns the start and end datetime for the given range_prop ('week', 'month', 'year').
    You can shift the base date back or forward using shift_months.
    """
    now = shift_date_by_months(datetime.now(), shift_months)

    if range_prop == "week":
        start = now - timedelta(days=now.weekday())
        end = start + timedelta(days=7)
    elif range_prop == "month":
        start = now.replace(day=1)
        if now.month == 12:
            end = now.replace(year=now.year + 1, month=1, day=1)
        else:
            end = now.replace(month=now.month + 1, day=1)
    elif range_prop == "year":
        start = now.replace(month=1, day=1)
        end = now.replace(year=now.year + 1, month=1, day=1)
    else:
        raise ValueError("range_prop must be 'week', 'month', or 'year'")

    return start.replace(tzinfo=None, microsecond=0), end.replace(tzinfo=None, microsecond=0)

def calculate_average_duration(region: str, range_prop: str, file_path: str) -> str:
    start, end = get_range_bounds(range_prop)
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    total_duration = 0
    alert_count = 0
    for alerts in data.values():
        for alert in alerts:
            if alert.get('location') == region:
                start_dt = datetime.fromisoformat(alert['start']).replace(tzinfo=None)
                end_dt = datetime.fromisoformat(alert['finish']).replace(tzinfo=None)
                if start <= start_dt < end:
                    total_duration += (end_dt - start_dt).total_seconds()
                    alert_count += 1
    if alert_count > 0:
        avg_minutes = (total_duration / alert_count) / 60
        if avg_minutes >= 60:
            hours = int(avg_minutes // 60)
            minutes = int(avg_minutes % 60)
            return f"{hours} год {minutes} хв"
        else:
            return f"{avg_minutes:.2f} хв"
    else:
        return "Не знайдено тривог для цієї області"

def count_alerts(region: str, range_prop: str, file_path: str) -> int:
    start, end = get_range_bounds(range_prop)
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    count = 0
    for alerts in data.values():
        for alert in alerts:
            if alert.get('location') == region:
                start_dt = datetime.fromisoformat(alert['start']).replace(tzinfo=None)
                if start <= start_dt < end:
                    count += 1
    return count

def calculate_alert_percentage(region: str, range_prop: str, file_path: str) -> float:
    start, end = get_range_bounds(range_prop)
    total_minutes = (end - start).total_seconds() / 60
    alert_minutes = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for alerts in data.values():
        for alert in alerts:
            if alert.get('location') == region:
                start_dt = datetime.fromisoformat(alert['start']).replace(tzinfo=None)
                end_dt = datetime.fromisoformat(alert['finish']).replace(tzinfo=None)
                if start <= start_dt < end:
                    effective_start = max(start, start_dt)
                    effective_end = min(end, end_dt)
                    if effective_end > effective_start:
                        alert_minutes += (effective_end - effective_start).total_seconds() / 60

    return (alert_minutes / total_minutes) * 100 if total_minutes > 0 else 0

def get_last_alert_time(region: str, file_path: str) -> str:
    ukr_months = [
        'січня', 'лютого', 'березня', 'квітня', 'травня', 'червня',
        'липня', 'серпня', 'вересня', 'жовтня', 'листопада', 'грудня'
    ]
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    last_start = None
    last_end = None

    for alerts in data.values():
        for alert in alerts:
            if alert.get('location') == region:
                start_dt = datetime.fromisoformat(alert['start']).replace(tzinfo=None)
                end_dt = datetime.fromisoformat(alert['finish']).replace(tzinfo=None)

                if last_start is None or start_dt > last_start:
                    last_start = start_dt
                    last_end = end_dt

    if last_start and last_end:
        start_str = last_start.strftime('%H:%M')
        end_str = last_end.strftime('%H:%M')
        date_str = f"{last_start.day} {ukr_months[last_start.month - 1]}"
        return f"{start_str} - {end_str}, {date_str}"
    return "Немає тривог для цієї області"

def plot_alert_durations_base64(region: str, range_prop: str, file_path: str) -> str:
    """
    Generates a bar chart of alert durations for a specific region and time range,
    aggregating data appropriately (daily for week/month, monthly for year).

    Args:
        region: The region name (e.g., "Хмельницька область").
        range_prop: The time range ('week', 'month', 'year').
        file_path: Path to the JSON file containing alert data.

    Returns:
        A base64 encoded PNG image string of the chart, or an empty string if no data.
    """
    start, end = get_range_bounds(range_prop)
    now = datetime.now()

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return ""
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}")
        return "" 

    ukr_months_short = [
        'Січ', 'Лют', 'Бер', 'Кві', 'Тра', 'Чер',
        'Лип', 'Сер', 'Вер', 'Жов', 'Лис', 'Гру'
    ]

    plot_data = {}
    aggregation_level = "daily"

    if range_prop == "year":
        aggregation_level = "monthly"
        plot_data = {m: 0 for m in range(1, 13)}
    elif range_prop == "month":
        aggregation_level = "daily"
        days_in_month = calendar.monthrange(start.year, start.month)[1]
        plot_data = { (start.date() + timedelta(days=i)): 0 for i in range(days_in_month) }
    elif range_prop == "week":
        aggregation_level = "daily"
        plot_data = { (start.date() + timedelta(days=i)): 0 for i in range(7) }

    for alerts_in_month in data.values():
        if not isinstance(alerts_in_month, list): continue

        for alert in alerts_in_month:
            if not all(k in alert for k in ['location', 'start', 'finish']):
                continue

            if alert.get('location') == region:
                try:
                    start_dt = datetime.fromisoformat(alert['start']).replace(tzinfo=None)
                    end_dt = datetime.fromisoformat(alert['finish']).replace(tzinfo=None)
                except (ValueError, TypeError):
                    continue

                if start_dt < end and end_dt > start:
                    effective_start = max(start, start_dt)
                    effective_end = min(end, end_dt)

                    if effective_end > effective_start:
                        current_segment_start = effective_start
                        while current_segment_start < effective_end:
                            duration_hours = 0
                            segment_end = effective_end

                            if aggregation_level == "monthly":
                                next_month_start_month = current_segment_start.month + 1
                                next_month_start_year = current_segment_start.year
                                if next_month_start_month > 12:
                                    next_month_start_month = 1
                                    next_month_start_year += 1
                                next_month_start_dt = datetime(next_month_start_year, next_month_start_month, 1)
                                segment_end = min(effective_end, next_month_start_dt)

                                if current_segment_start.year == start.year:
                                     month_key = current_segment_start.month
                                     duration_hours = (segment_end - current_segment_start).total_seconds() / 3600
                                     plot_data[month_key] = plot_data.get(month_key, 0) + duration_hours

                            elif aggregation_level == "daily":
                                next_day_start = datetime.combine(current_segment_start.date() + timedelta(days=1), datetime.min.time())
                                segment_end = min(effective_end, next_day_start)

                                day_key = current_segment_start.date()
                                if day_key in plot_data:
                                     duration_hours = (segment_end - current_segment_start).total_seconds() / 3600
                                     plot_data[day_key] = plot_data.get(day_key, 0) + duration_hours

                            current_segment_start = segment_end


    if not plot_data or all(value == 0 for value in plot_data.values()):
         print(f"No alert data to plot for {region} in range {range_prop}")
         return ""

    sorted_keys = sorted(plot_data.keys())
    durations = [plot_data[key] for key in sorted_keys]

    fig, ax = plt.subplots(figsize=(12, 6))
    bar_color = '#a94442'
    title = f'Сумарна тривалість тривог (год) - {region}'
    x_label = 'Дата'
    y_label = 'Тривалість (години)'
    rotation = 45
    label_format = "%d.%m"
    locator = mticker.AutoLocator()

    if range_prop == "year":
        full_year_data = {m: plot_data.get(m, 0) for m in range(1, 13)}
        sorted_keys = sorted(full_year_data.keys())
        durations = [full_year_data[key] for key in sorted_keys]
        labels = [ukr_months_short[key - 1] for key in sorted_keys]

        title = f'{title}\nЗа місяцями, {start.year} рік'
        x_label = 'Місяць'
        rotation = 0

    elif range_prop == "month":
        labels = [key.strftime(label_format) for key in sorted_keys]
        title = f'{title}\nПо днях, {ukr_months_short[start.month-1].lower()} {start.year}'
        rotation = 90
        if len(labels) > 15:
             locator = mticker.MultipleLocator(base=3)
        elif len(labels) > 7:
             locator = mticker.MultipleLocator(base=2)


    elif range_prop == "week":
        labels = [key.strftime(label_format) for key in sorted_keys]
        title = f'{title}\nПо днях, тиждень від {start.strftime(label_format)}'
        rotation = 45

    ax.bar(range(len(labels)), durations, color=bar_color)

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=rotation, ha='right' if rotation >= 45 else ('center' if rotation == 0 else 'left'))
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    ax.xaxis.set_major_locator(locator)

    for i, v in enumerate(durations):
        if v > 0:
            label_text = f"{v:.1f}" if v % 1 != 0 else f"{int(v)}"
            ax.text(i, v + (max(durations) * 0.01), label_text, ha='center', va='bottom', fontsize=8, rotation=90)


    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=90)
    plt.close(fig) 
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

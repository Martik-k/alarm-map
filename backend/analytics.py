import base64
from io import BytesIO
import json
from datetime import datetime, timedelta
import calendar # Needed for month names/days
import matplotlib
matplotlib.use('Agg') # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker # To control label frequency

# --- get_range_bounds remains the same ---
def get_range_bounds(range_prop: str) -> tuple[datetime, datetime]:
    """
    Returns the start and end datetime for the given range_prop ('week', 'month', 'year').
    These are naive datetimes.
    """
    now = datetime.now()
    if range_prop == "week":
        start = now - timedelta(days=now.weekday())  # Monday of this week
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
    # Ensure start and end are naive and without microseconds for clean comparison
    return start.replace(tzinfo=None, microsecond=0), end.replace(tzinfo=None, microsecond=0)

# --- calculate_average_duration corrected ---
def calculate_average_duration(region: str, range_prop: str, file_path: str) -> str:
    start, end = get_range_bounds(range_prop) # Naive datetimes
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    total_duration = 0
    alert_count = 0
    for alerts in data.values():
        for alert in alerts:
            if alert.get('location') == region:
                # Read as aware, then make naive
                start_dt = datetime.fromisoformat(alert['start']).replace(tzinfo=None)
                end_dt = datetime.fromisoformat(alert['finish']).replace(tzinfo=None)
                # Compare naive with naive
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

# --- count_alerts corrected ---
def count_alerts(region: str, range_prop: str, file_path: str) -> int:
    start, end = get_range_bounds(range_prop) # Naive datetimes
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    count = 0
    for alerts in data.values():
        for alert in alerts:
            if alert.get('location') == region:
                # Read as aware, then make naive
                start_dt = datetime.fromisoformat(alert['start']).replace(tzinfo=None)
                # Compare naive with naive
                if start <= start_dt < end:
                    count += 1
    return count

# --- calculate_alert_percentage corrected ---
def calculate_alert_percentage(region: str, range_prop: str, file_path: str) -> float:
    start, end = get_range_bounds(range_prop) # Naive datetimes
    total_minutes = (end - start).total_seconds() / 60
    alert_minutes = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for alerts in data.values():
        for alert in alerts:
            if alert.get('location') == region:
                # Read as aware, then make naive
                start_dt = datetime.fromisoformat(alert['start']).replace(tzinfo=None)
                end_dt = datetime.fromisoformat(alert['finish']).replace(tzinfo=None)
                # Compare naive with naive
                if start <= start_dt < end:
                     # Consider alerts spanning the boundary: Clip duration to the range
                     effective_start = max(start, start_dt)
                     effective_end = min(end, end_dt)
                     if effective_end > effective_start: # Ensure valid duration within range
                         alert_minutes += (effective_end - effective_start).total_seconds() / 60

    return (alert_minutes / total_minutes) * 100 if total_minutes > 0 else 0

# --- get_last_alert_time corrected (optional, but good practice) ---
def get_last_alert_time(region: str, file_path: str) -> str:
    ukr_months = [
        'січня', 'лютого', 'березня', 'квітня', 'травня', 'червня',
        'липня', 'серпня', 'вересня', 'жовтня', 'листопада', 'грудня'
    ]
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    last_start = None # Will store naive datetime
    last_end = None   # Will store naive datetime

    for alerts in data.values():
        for alert in alerts:
            if alert.get('location') == region:
                # Read as aware, then make naive
                start_dt = datetime.fromisoformat(alert['start']).replace(tzinfo=None)
                end_dt = datetime.fromisoformat(alert['finish']).replace(tzinfo=None)

                if last_start is None or start_dt > last_start:
                    last_start = start_dt
                    last_end = end_dt
                    # last_date is not needed, can derive from last_start

    if last_start and last_end: # Ensure both are found
        start_str = last_start.strftime('%H:%M')
        end_str = last_end.strftime('%H:%M')
        date_str = f"{last_start.day} {ukr_months[last_start.month - 1]}"
        return f"{start_str} - {end_str}, {date_str}"
    return "Немає тривог для цієї області"

# --- plot_alert_durations_base64 corrected ---
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
    start, end = get_range_bounds(range_prop) # Naive datetimes
    now = datetime.now() # Needed for year range calculation

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return "" # Return empty if file doesn't exist
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}")
        return "" # Return empty if JSON is invalid

    # Ukrainian month abbreviations
    ukr_months_short = [
        'Січ', 'Лют', 'Бер', 'Кві', 'Тра', 'Чер',
        'Лип', 'Сер', 'Вер', 'Жов', 'Лис', 'Гру'
    ]

    # --- Data Aggregation ---
    plot_data = {} # Key depends on range_prop (date for week/month, month number for year)
    aggregation_level = "daily" # Default

    # Initialize plot_data with zeros for the entire range
    if range_prop == "year":
        aggregation_level = "monthly"
        plot_data = {m: 0 for m in range(1, 13)} # Keys are month numbers (1-12)
    elif range_prop == "month":
        aggregation_level = "daily"
        days_in_month = calendar.monthrange(start.year, start.month)[1]
        plot_data = { (start.date() + timedelta(days=i)): 0 for i in range(days_in_month) } # Keys are date objects
    elif range_prop == "week":
        aggregation_level = "daily"
        plot_data = { (start.date() + timedelta(days=i)): 0 for i in range(7) } # Keys are date objects

    # Process alerts from JSON
    for alerts_in_month in data.values(): # Assumes JSON structure like {"month_num_str": [alerts...]}
        if not isinstance(alerts_in_month, list): continue # Skip if value is not a list of alerts

        for alert in alerts_in_month:
             # Basic check for essential keys
            if not all(k in alert for k in ['location', 'start', 'finish']):
                continue # Skip malformed alert entries

            if alert.get('location') == region:
                try:
                    # Read as aware (if timezone info present), then make naive
                    start_dt = datetime.fromisoformat(alert['start']).replace(tzinfo=None)
                    end_dt = datetime.fromisoformat(alert['finish']).replace(tzinfo=None)
                except (ValueError, TypeError):
                    continue # Skip if date parsing fails

                # Check if the alert overlaps with the requested range [start, end)
                if start_dt < end and end_dt > start:
                    # Clip the alert duration to the requested range
                    effective_start = max(start, start_dt)
                    effective_end = min(end, end_dt)

                    if effective_end > effective_start: # Ensure there's duration within the range
                        # --- Aggregate based on level ---
                        current_segment_start = effective_start
                        while current_segment_start < effective_end:
                            duration_hours = 0
                            # Determine the end of the current segment (day or month)
                            # or the end of the alert within the range, whichever comes first.
                            segment_end = effective_end # Default unless crossing boundary

                            if aggregation_level == "monthly":
                                next_month_start_month = current_segment_start.month + 1
                                next_month_start_year = current_segment_start.year
                                if next_month_start_month > 12:
                                    next_month_start_month = 1
                                    next_month_start_year += 1
                                next_month_start_dt = datetime(next_month_start_year, next_month_start_month, 1)
                                segment_end = min(effective_end, next_month_start_dt)

                                # Add duration to the correct month's total
                                if current_segment_start.year == start.year: # Ensure it's within the plot year
                                     month_key = current_segment_start.month
                                     duration_hours = (segment_end - current_segment_start).total_seconds() / 3600
                                     plot_data[month_key] = plot_data.get(month_key, 0) + duration_hours

                            elif aggregation_level == "daily":
                                next_day_start = datetime.combine(current_segment_start.date() + timedelta(days=1), datetime.min.time())
                                segment_end = min(effective_end, next_day_start)

                                # Add duration to the correct day's total
                                day_key = current_segment_start.date()
                                if day_key in plot_data: # Check if day is within the initialized range
                                     duration_hours = (segment_end - current_segment_start).total_seconds() / 3600
                                     plot_data[day_key] = plot_data.get(day_key, 0) + duration_hours

                            # Move to the start of the next segment
                            current_segment_start = segment_end


    # --- Plotting ---
    # Check if there is any data to plot after aggregation
    if not plot_data or all(value == 0 for value in plot_data.values()):
         print(f"No alert data to plot for {region} in range {range_prop}") # Debugging info
         # Optionally: generate a placeholder image saying "No data"
         # For now, return empty string
         return ""

    # Prepare data for plotting
    sorted_keys = sorted(plot_data.keys())
    durations = [plot_data[key] for key in sorted_keys]

    # --- Customize plot based on range ---
    fig, ax = plt.subplots(figsize=(12, 6)) # Slightly wider figure, get axis object
    bar_color = '#a94442'
    title = f'Сумарна тривалість тривог (год) - {region}'
    x_label = 'Дата'
    y_label = 'Тривалість (години)'
    rotation = 45
    label_format = "%d.%m" # Default for daily
    locator = mticker.AutoLocator() # Default: let matplotlib decide tick frequency

    if range_prop == "year":
        # Ensure all 12 months are represented for consistent plotting if any data exists
        full_year_data = {m: plot_data.get(m, 0) for m in range(1, 13)}
        sorted_keys = sorted(full_year_data.keys())
        durations = [full_year_data[key] for key in sorted_keys]
        labels = [ukr_months_short[key - 1] for key in sorted_keys] # Month abbreviations

        title = f'{title}\nЗа місяцями, {start.year} рік'
        x_label = 'Місяць'
        rotation = 0 # No rotation needed for 12 labels

    elif range_prop == "month":
        labels = [key.strftime(label_format) for key in sorted_keys] # DD.MM format
        title = f'{title}\nПо днях, {ukr_months_short[start.month-1].lower()} {start.year}'
        rotation = 90 # Rotate fully for potentially ~30 labels
        # Adjust tick frequency if too many labels
        if len(labels) > 15: # Heuristic: if more than 15 days
             locator = mticker.MultipleLocator(base=3) # Show roughly every 3rd day label
        elif len(labels) > 7:
             locator = mticker.MultipleLocator(base=2) # Show roughly every 2nd day label


    elif range_prop == "week":
        labels = [key.strftime(label_format) for key in sorted_keys] # DD.MM format
        title = f'{title}\nПо днях, тиждень від {start.strftime(label_format)}'
        rotation = 45 # 45 degrees is fine for 7 labels

    # Create the bar chart
    ax.bar(range(len(labels)), durations, color=bar_color) # Use numeric index for bars

    # Apply formatting
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xticks(range(len(labels))) # Set tick positions
    ax.set_xticklabels(labels, rotation=rotation, ha='right' if rotation >= 45 else ('center' if rotation == 0 else 'left')) # Set tick labels
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Apply the locator to adjust tick frequency if needed (esp. for month)
    ax.xaxis.set_major_locator(locator)

    # Add value labels on top of bars if space permits and value > 0
    for i, v in enumerate(durations):
        if v > 0: # Only label bars with value > 0
            # Format label to 1 decimal place if needed, or integer
            label_text = f"{v:.1f}" if v % 1 != 0 else f"{int(v)}"
            ax.text(i, v + (max(durations) * 0.01), label_text, ha='center', va='bottom', fontsize=8, rotation=90)


    fig.tight_layout() # Adjust layout

    # Save to buffer
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=90) # Use the figure object to save
    plt.close(fig) # Close the specific figure to free memory
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

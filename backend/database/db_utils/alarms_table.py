"""
Module for managing and querying alarm data in the database.
"""

from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta  # потрібно встановити: pip install python-dateutil
from ..models import db, Alarm
from zoneinfo import ZoneInfo
from sqlalchemy import or_

LOCATIONS = ["Vinnytska", "Volynska", "Dnipropetrovska", "Donetska", "Zhytomyrska", "Zakarpatska",
             "Zaporizka", "Ivano-Frankivska", "Kyivska", "Kirovohradska", "Luhanska",
             "Lvivska", "Mykolaivska", "Odeska", "Poltavska", "Rivnenska", "Sumska",
             "Ternopilska", "Kharkivska", "Khersonska", "Khmelnytska", "Cherkaska",
             "Chernihivska", "Chernivetska", "Kyiv", "Avtonomna Respublika Krym", "Kyiv"]


def get_kyiv_time():
    now_kyiv = datetime.now(ZoneInfo("Europe/Kyiv"))
    return now_kyiv.replace(tzinfo=None)


def find_start_period(period: str, end):
    """
    Calculates the start datetime for a given period relative to an end datetime.

    Args:
        period (str): The time period ('week', 'month', or 'year').
        end (datetime): The reference end datetime.

    Returns:
        datetime: The calculated start datetime.

    Raises:
        ValueError: If an unknown period is provided.
    """
    if period == "week":
        start = end - timedelta(weeks=1)
    elif period == "month":
        start = end - relativedelta(months=1)
    elif period == "year":
        start = end - relativedelta(years=1)
    else:
        raise ValueError("Unknown period")
    return start


def clear_alarms_table(app):
    """
    Clears all records from the Alarm table in the database.

    Args:
        app (Flask): The Flask application instance.
    """
    with app.app_context():
        db.session.query(Alarm).delete()
        db.session.commit()


def add_alarm(app, start,  finish, location, is_active):
    """
    Adds a new alarm record to the database.

    Args:
        app (Flask): The Flask application instance.
        start (datetime): The start datetime of the alarm.
        finish (datetime): The finish datetime of the alarm (can be None if active).
        location (str): The geographical location of the alarm.
        is_active (bool): A boolean indicating if the alarm is currently active.
    """
    with app.app_context():
        new_alarm = Alarm(start=start, location=location, finish=finish, is_active=is_active)
        db.session.add(new_alarm)
        db.session.commit()


def update_alarm_finish(app, alarm_id, finish):
    """
    Updates the finish datetime and sets is_active to False for a specific alarm record.

    Args:
        app (Flask): The Flask application instance.
        alarm_id (int): The ID of the alarm record to update.
        finish (datetime): The finish datetime of the alarm.
    """
    with app.app_context():
        alarm = db.session.get(Alarm, alarm_id)
        if alarm:
            alarm.finish = finish
            alarm.is_active = False
            db.session.commit()


def process_alarm_data(app, alarm_data: dict[str: str], time):   # alarm_data = {'Lvivska': 'alarm'}
    """
    Processes incoming alarm data, adding new active alarms and updating the finish
    time for alarms that have ended.

    Args:
        app (Flask): The Flask application instance.
        alarm_data (dict[str, str]): A dictionary where keys are locations and
                                     values are the alarm status ('alarm' or other).
        time (datetime): The current datetime when the data was received.

    Returns:
        tuple[list[Alarm], list[Alarm]]: A tuple containing two lists:
            - new_alarms (list[Alarm]): A list of newly started or still active alarms.
            - finished_alarms (list[Alarm]): A list of alarms that have just finished.
    """
    with app.app_context():
        active_alarms = {a.location: a for a in Alarm.query.filter_by(is_active=True).all()}

    new_alarms = []
    finished_alarms = []

    for location, status in alarm_data.items():
        if status == "alarm":
            if location not in active_alarms:
                add_alarm(app, start=time, location=location, finish=None, is_active=True)
                new_alarms.append({'location': location, 'start': time})
            else:
                new_alarms.append(active_alarms[location])
            active_alarms.pop(location, None)

    for a in active_alarms.values():
        if a.location in alarm_data and alarm_data[a.location] != "alarm":
            update_alarm_finish(app, a.id, time)
            finished_alarms.append(a)

    return new_alarms, finished_alarms


def get_all_periods_starts(period, end):
    """
    Generates a list of start datetimes for plotting analytics over a given period.

    Args:
        period (str): The time period ('week', 'month', or 'year').
        now (datetime): The current datetime.

    Returns:
        list[datetime]: A list of datetime objects representing the start of each
                       interval for the plot.
    """
    plot_periods_starts = []

    if period == "week":
        for days in range(7, -2, -1): # CHANGE -2 TO -1
            start = end - timedelta(days=days)
            plot_periods_starts.append(start)
    elif period == "month":
        start = end - relativedelta(months=1)
        delta_days = (end - start).days
        for days in range(delta_days, -2, -1):
            start = end - timedelta(days=days)
            plot_periods_starts.append(start)
    elif period == "year":
        end = end.replace(day=1)
        for months in range(11, -2, -1):
            start = end - relativedelta(months=months)
            plot_periods_starts.append(start)
    return plot_periods_starts


def get_alarms_for_period(app, period: str, last_date):
    """
    Retrieves the count and total duration of alarms for each location within a given period.
    """
    now = get_kyiv_time()
    end = now.replace(hour=0, minute=0, second=0, microsecond=0)
    start_all_periods = get_all_periods_starts(period, end)
    start_all_period = start_all_periods[0]

    start_getting = max(start_all_period, last_date)
    alarms = None
    with app.app_context():
        alarms = Alarm.query.filter(
            db.or_(Alarm.finish == None, Alarm.finish > start_getting)
        ).all()

    total_counts_durations = {
        location: [
            0,  # alarm count
            timedelta(0),  # total duration
            datetime(2022, 1, 1),  # latest finish time
            {start: timedelta(0) for start in start_all_periods[:-1]}  # durations per day
        ]
        for location in LOCATIONS
    }

    for alarm in alarms:
        alarm_start = max(alarm.start, start_all_period)
        alarm_finish = end if alarm.finish is None else alarm.finish

        total_counts_durations[alarm.location][0] += 1
        total_counts_durations[alarm.location][1] += alarm_finish - alarm_start
        total_counts_durations[alarm.location][2] = max(
            total_counts_durations[alarm.location][2], alarm_finish
        )


        for i, start_period in enumerate(start_all_periods[:-1]):
            finish_period = start_all_periods[i + 1]

            if alarm_finish <= start_period or alarm_start >= finish_period:
                continue

            start_alarm_period = max(alarm_start, start_period)
            finish_alarm_period = min(alarm_finish, finish_period)
            duration = finish_alarm_period - start_alarm_period

            total_counts_durations[alarm.location][3][start_period] += duration
        
        total_counts_durations['Kyiv'] = total_counts_durations['Kyivska']
    return total_counts_durations, start_all_period


def create_alarms_dictionary(app, last_date):
    """
    Creates a dictionary containing alarm counts and durations 
    for 'week', 'month', and 'year' periods.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        dict[str, dict[str, list]]: A dictionary where keys are time periods 
                                     ('week', 'month', 'year') and values are 
                                     dictionaries of location-based alarm data
                                     (as returned by get_alarms_counts_durations_for_period).
    """
    result = {}
    result_starts = {}
    for period in ['week', 'month', 'year']:
        result[period], result_starts[period] = get_alarms_for_period(app, period, last_date)
    return result, result_starts

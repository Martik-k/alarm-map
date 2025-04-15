# db_utils/alarms.py

from datetime import datetime, timedelta
from ..models import db, Alarm
from flask import current_app
from copy import deepcopy


LOCATIONS_ALARM_COUNT_DURATION = {
    "Vinnytska": [0, timedelta(0)],
    "Volynska": [0, timedelta(0)],
    "Dnipropetrovska": [0, timedelta(0)],
    "Donetska": [0, timedelta(0)],
    "Zhytomyrska": [0, timedelta(0)],
    "Zakarpatska": [0, timedelta(0)],
    "Zaporizka": [0, timedelta(0)],
    "Ivano-Frankivska": [0, timedelta(0)],
    "Kyivska": [0, timedelta(0)],
    "Kirovohradska": [0, timedelta(0)],
    "Luhanska": [0, timedelta(0)],
    "Lvivska": [0, timedelta(0)],
    "Mykolaivska": [0, timedelta(0)],
    "Odeska": [0, timedelta(0)],
    "Poltavska": [0, timedelta(0)],
    "Rivnenska": [0, timedelta(0)],
    "Sumska": [0, timedelta(0)],
    "Ternopilska": [0, timedelta(0)],
    "Kharkivska": [0, timedelta(0)],
    "Khersonska": [0, timedelta(0)],
    "Khmelnytska": [0, timedelta(0)],
    "Cherkaska": [0, timedelta(0)],
    "Chernihivska": [0, timedelta(0)],
    "Chernivetska": [0, timedelta(0)],
    "Kyiv": [0, timedelta(0)],
    "Avtonomna Respublika Krym": [0, timedelta(0)]
}

def get_alarms_by_location(location):
    return Alarm.query.filter_by(location=location).all()

def add_alarm(start, location, finish, is_active):
    new_alarm = Alarm(start=start, location=location, finish=finish, is_active=is_active)
    db.session.add(new_alarm)
    db.session.commit()

def update_alarm_finish(alarm_id, finish):
    alarm = db.session.get(Alarm, alarm_id)
    if alarm:
        alarm.finish = finish
        alarm.is_active = False
        db.session.commit()

def process_alarm_data(alarm_data: dict[str: str], time):   # alarm_data = {'Lvivska': 'alarm'}
    active_alarms = {a.location: a for a in Alarm.query.filter_by(is_active=True).all()}
    new_alarms = []
    finished_alarms = []

    for location, status in alarm_data.items():
        if status == "alarm":
            if location not in active_alarms:
                add_alarm(start=time, location=location, finish=None, is_active=True)
                new_alarms.append({'location': location, 'start': time})
            else:
                new_alarms.append(active_alarms[location])
            active_alarms.pop(location, None)

    for a in active_alarms.values():
        if a.finish is None or a.finish < time:
            update_alarm_finish(a.id, time)
            finished_alarms.append(a)

    return new_alarms, finished_alarms


def get_alarms_counts_durations_for_period(period: str):   # period is 'week', 'month' or 'year'
    now = datetime.now()
    match period:
        case 'week':
            start_period = now - timedelta(days=now.weekday())
        case 'month':
            start_period = now.replace(day=1)
        case 'year':
            start_period = now.replace(month=1, day=1)
        case _:
            raise ValueError
    
    with current_app.app_context():
        alarms = Alarm.query.filter(
            db.or_(Alarm.finish == None, Alarm.finish > start_period)
        ).all()

        total_counts_durations = deepcopy(LOCATIONS_ALARM_COUNT_DURATION)
        for alarm in alarms:
            finish = alarm.finish if alarm.finish else now
            start = max(alarm.start, start_period)
            total_counts_durations[alarm.location][0] += 1
            total_counts_durations[alarm.location][1] += finish - start

    return total_counts_durations

def create_dictionary():
    result = {}
    for period in ['week', 'month', 'year']:
        result[period] = get_alarms_counts_durations_for_period(period)
    return result
    

    
    

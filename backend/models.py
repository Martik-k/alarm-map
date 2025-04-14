from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timedelta

db = SQLAlchemy()
migrate = Migrate(db)

class Alarm(db.Model):
    __tablename__ = 'alarms'

    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    finish = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Alarm {self.location} - {self.start}>'

def get_alarms_by_location(app, location):
    with app.app_context():
        alarms = Alarm.query.filter_by(location=location).all()
        return alarms

def add_alarm(app, start, location, finish, is_active):
    with app.app_context():
        new_alarm = Alarm(start=start, location=location, finish=finish, is_active=is_active)
        db.session.add(new_alarm)
        db.session.commit()

def clear_alarm_table(app):
    with app.app_context():
        Alarm.query.delete()
        db.session.commit()

def update_alarm_finish(app, alarm_id, finish):
    with app.app_context():
        alarm = db.session.get(Alarm, alarm_id)
        if alarm:
            alarm.finish = finish
            alarm.is_active = False
            db.session.commit()


def process_alarm_data(app, alarm_data, time):
    with app.app_context():
        active_alarms = {alarm.location: alarm for alarm in Alarm.query.filter_by(is_active=True).all()}

        new_alarms = []
        finished_alarms = []

        current_time = time

        for location, status in alarm_data.items():
            if status == "alarm":
                start = current_time

                active_alarm = active_alarms.get(location)

                if active_alarm:
                    new_alarms.append(active_alarm)
                else:
                    add_alarm(app, start, location, None, True)
                    new_alarms.append({'location': location, 'start': start})

                active_alarms.pop(location, None)

        for existing_alarm in active_alarms.values():
            if existing_alarm.finish is None or existing_alarm.finish < current_time:
                update_alarm_finish(app, existing_alarm.id, current_time)
                finished_alarms.append(existing_alarm)

        return new_alarms, finished_alarms


def get_alarm_data_from_db_days_ago(app, current_time_str, number_days):
    with app.app_context():
        current_time = datetime.strptime(current_time_str, '%Y-%m-%d %H:%M:%S')
        days_ago = current_time - timedelta(days=number_days)

        alarms = Alarm.query.filter(Alarm.start >= days_ago).all()

        alarm_counts = {}
        for alarm in alarms:
            if alarm.location in alarm_counts:
                alarm_counts[alarm.location] += 1
            else:
                alarm_counts[alarm.location] = 1

        return alarm_counts



class Shelling(db.Model):
    __tablename__ = 'shellings'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    location = db.Column(db.String(50))

    def __repr__(self):
        return f'<Shelling {self.location} - {self.time}>'


def clear_shelling_table(app):
    with app.app_context():
        Shelling.query.delete()
        db.session.commit()


def process_shelling_data(app, shelling_data: list[dict[str, str]]):
    with app.app_context():
        for shelling in shelling_data:
            datetime_str = f"{shelling['date']} {shelling['time']}"
            datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')

            new_alarm = Shelling(time=datetime_object, location=shelling['city'])
            db.session.add(new_alarm)
            db.session.commit()


def get_shelling_data_from_db_days_ago(app, current_time_str, number_days):
    with app.app_context():
        current_time = datetime.strptime(current_time_str, '%Y-%m-%d %H:%M')
        one_month_ago = current_time - timedelta(days=number_days)

        shellings = Shelling.query.filter(Shelling.time >= one_month_ago).all()

        shelling_counts = {}
        for shelling in shellings:
            if shelling.location in shelling_counts:
                shelling_counts[shelling.location] += 1
            else:
                shelling_counts[shelling.location] = 1

        return shelling_counts

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate(db)

class Alarm(db.Model):
    __tablename__ = 'alarms'

    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String(50))
    finish = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(50))
    location_type = db.Column(db.String(50))
    type = db.Column(db.String(50), nullable=False)


    def __repr__(self):
        return f'<Alarm {self.location} - {self.start}>'

def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)


def get_alarms_by_location(app, location):
    with app.app_context():
        alarms = Alarm.query.filter_by(location=location).all()
        return alarms


def add_alarm(app, start, location, finish, location_type, type):
    with app.app_context():
        new_alarm = Alarm(start=start, location=location, finish=finish, location_type=location_type, type=type)
        db.session.add(new_alarm)
        db.session.commit()


def clear_alarm_table(app):
    with app.app_context():
        Alarm.query.delete()
        db.session.commit()


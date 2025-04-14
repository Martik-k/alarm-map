import unittest
from app import app
from models import db, Alarm, process_alarm_data
from datetime import datetime

def print_alarms_table():
    with app.app_context():
        alarms = Alarm.query.all()
        for alarm in alarms:
            print(f"ID: {alarm.id}, Location: {alarm.location}, Start: {alarm.start}, Finish: {alarm.finish}, is_active: {alarm.is_active}")

class TestProcessAlarmData(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_new_alarms(self):
        with app.app_context():
            alarm_data = {
                'Kyiv': 'alarm',
                'Lviv': 'alarm',
            }
            time = '16:00:00'
            new_alarms, finished_alarms = process_alarm_data(app, alarm_data, time)
            self.assertEqual(len(new_alarms), 2)
            self.assertEqual(len(finished_alarms), 0)
            self.assertEqual(Alarm.query.count(), 2)
            print('test_new_alarms')
            print_alarms_table()

    def test_finished_alarms(self):
        with app.app_context():
            alarm = Alarm(location='Kyiv', start='09:00:00', is_active=True)
            db.session.add(alarm)
            db.session.commit()
            alarm_data = {
                'Lviv': 'alarm',
            }
            time = '16:00:00'
            new_alarms, finished_alarms = process_alarm_data(app, alarm_data, time)
            self.assertEqual(len(new_alarms), 1)
            self.assertEqual(len(finished_alarms), 1)
            self.assertFalse(Alarm.query.filter_by(location='Kyiv').first().is_active)
            self.assertEqual(Alarm.query.filter_by(location='Kyiv').first().finish, time)
            print('test_finished_alarms')
            print_alarms_table()

    def test_existing_active_alarm(self):
        with app.app_context():
            alarm = Alarm(location='Kyiv', start='10:00:00', is_active=True)
            db.session.add(alarm)
            db.session.commit()
            alarm_data = {
                'Kyiv': 'alarm',
            }
            time = '16:00:00'
            new_alarms, finished_alarms = process_alarm_data(app, alarm_data, time)
            self.assertEqual(len(new_alarms), 1)
            self.assertEqual(len(finished_alarms), 0)
            self.assertEqual(Alarm.query.count(), 1)
            print('test_existing_active_alarm')
            print_alarms_table()

    def test_existing_inactive_alarm(self):
        with app.app_context():
            alarm = Alarm(location='Kyiv', start='10:00:00', finish='12:00:00', is_active=False)
            db.session.add(alarm)
            db.session.commit()
            alarm_data = {
                'Lviv': 'alarm', # зміна локації
            }
            time = '16:00:00'
            new_alarms, finished_alarms = process_alarm_data(app, alarm_data, time)
            self.assertEqual(len(new_alarms), 1)
            self.assertEqual(len(finished_alarms), 0)
            self.assertEqual(Alarm.query.count(), 2)
            self.assertFalse(Alarm.query.filter_by(location='Kyiv').first().is_active)
            print('test_existing_inactive_alarm')
            print_alarms_table()

    def test_alarm_finished_before_new_start(self):
        with app.app_context():
            alarm = Alarm(location='Kyiv', start='12:00:00', finish=None, is_active=True)
            db.session.add(alarm)
            db.session.commit()
            alarm_data = {
                'Kyiv': 'alarm',
            }
            time = '16:00:00'
            new_alarms, finished_alarms = process_alarm_data(app, alarm_data, time)
            print('test_alarm_finished_before_new_start')
            print_alarms_table()
            self.assertEqual(len(new_alarms), 1)
            self.assertEqual(len(finished_alarms), 0)
            self.assertEqual(Alarm.query.count(), 1)
            self.assertTrue(Alarm.query.filter_by(location='Kyiv').first().is_active)
            self.assertEqual(Alarm.query.filter_by(location='Kyiv').first().start, '12:00:00')

if __name__ == '__main__':
    unittest.main()
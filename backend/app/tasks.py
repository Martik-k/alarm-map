import time
from datetime import datetime
from utils.news import get_news
from utils.alerts_services import get_active_alerts
from database.db_utils.alarms import process_alarm_data

news_data = ""
current_time = datetime.now()

def get_data(app):
    global news_data, current_time
    while True:
        with app.app_context():
            app.config['ALARM_DATA'] = get_active_alerts()
            news_data = get_news()
            current_time = datetime.now()
        time.sleep(30)

def update_database(app):
    while True:
        with app.app_context():
            alarm_data = app.config.get('ALARM_DATA', {})
            process_alarm_data(alarm_data, current_time)
            print('update')
        time.sleep(30)
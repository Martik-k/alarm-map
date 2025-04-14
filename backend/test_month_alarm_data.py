from app import app
from models import get_alarm_data_from_db_days_ago, clear_alarm_table

print(get_alarm_data_from_db_days_ago(app, "2025-04-17 23:55:00", 30))
clear_alarm_table(app)
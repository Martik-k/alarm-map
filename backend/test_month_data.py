from app import app
from models import get_data_from_db_days_ago

print(get_data_from_db_days_ago(app, "2023-10-27 23:55:00", 30))
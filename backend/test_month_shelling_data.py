from app import app
from models import get_shelling_data_from_db_days_ago, process_shelling_data, clear_shelling_table

shelling_data=[{'date': '2025-04-13', 'time': '21:58', 'city': 'Kirovohradska'}, 
               {'date': '2025-04-13', 'time': '21:58', 'city': 'Cherkaska'}, 
               {'date': '2025-04-13', 'time': '21:27', 'city': 'Kirovohradska'}, 
               {'date': '2025-04-13', 'time': '21:27', 'city': 'Mykolaivska'}, 
               {'date': '2025-04-13', 'time': '21:27', 'city': 'Cherkaska'}, 
               {'date': '2025-04-13', 'time': '21:12', 'city': 'Dnipropetrovska'}, 
               {'date': '2025-04-13', 'time': '21:12', 'city': 'Kirovohradska'}, 
               {'date': '2025-04-13', 'time': '20:56', 'city': 'Kirovohradska'}, 
               {'date': '2025-04-13', 'time': '20:49', 'city': 'Donetska'}]

process_shelling_data(app, shelling_data)
print(get_shelling_data_from_db_days_ago(app, "2025-04-17 23:55", 30))
clear_shelling_table(app)

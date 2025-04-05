import sqlite3
from app import app

conn = sqlite3.connect('instance/active_alerts.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM alarms')
rows = cursor.fetchall()
print(rows)

conn.close()
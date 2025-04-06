from datetime import datetime
from models import db, init_db
from flask import Flask, render_template
from models import db, init_db, add_alarm, clear_alarm_table
import re
import alarm
import getting_news
import time

app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///active_alerts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)

# Ініціалізація глобальної змінної
alarm_data_1 = {}
news = getting_news.get_news()
current_time  = "00:00:00"
def get_data():
    global alarm_data_1
    global current_time 
    while True:
        alarm_data_1 = alarm.get_active_alerts()
        accure_time = datetime.now().time()
        current_time = re.findall(r'..:..:..', f"{accure_time}")[0]
        time.sleep(30)


danger_data_1= {
    "Vinnytska": "notdanger",
    "Volynska": "danger",
    "Dnipropetrovska": "lessdanger",
    "Donetska": "danger",
    "Zhytomyrska": "notdanger",
    "Zakarpatska": "notdanger",
    "Zaporizka": "lessdanger",
    "Ivano-Frankivska": "notdanger",
    "Kyivska": "lessdanger",
    "Kirovohradska": "notdanger",
    "Luhanska": "danger",
    "Lvivska": "notdanger",
    "Mykolaivska": "lessdanger",
    "Odeska": "lessdanger",
    "Poltavska": "notdanger",
    "Rivnenska": "lessdanger",
    "Sumska": "danger",
    "Ternopilska": "lessdanger",
    "Kharkivska": "danger",
    "Khersonska": "lessdanger",
    "Khmelnytska": "notdanger",
    "Cherkaska": "lessdanger ",
    "Chernihivska": "notdanger",
    "Chernivetska": "lessdanger ",
    "Kyiv": "lessdanger",
    "Avtonomna Respublika Krym" : "lessdanger"
}

danger_data_2= {
    "Vinnytska": "notdanger",
    "Volynska": "danger",
    "Dnipropetrovska": "danger",
    "Donetska": "danger",
    "Zhytomyrska": "notdanger",
    "Zakarpatska": "danger",
    "Zaporizka": "danger",
    "Ivano-Frankivska": "notdanger",
    "Kyivska": "lessdanger",
    "Kirovohradska": "notdanger",
    "Luhanska": "danger",
    "Lvivska": "notdanger",
    "Mykolaivska": "lessdanger",
    "Odeska": "lessdanger",
    "Poltavska": "notdanger",
    "Rivnenska": "danger",
    "Sumska": "danger",
    "Ternopilska": "lessdanger",
    "Kharkivska": "danger",
    "Khersonska": "lessdanger",
    "Khmelnytska": "notdanger",
    "Cherkaska": "lessdanger ",
    "Chernihivska": "ndanger",
    "Chernivetska": "lessdanger ",
    "Kyiv": "lessdanger",
    "Avtonomna Respublika Krym" : "lessdanger"
}

@app.route("/")
@app.route("/alarm_map")
def home():
    # accure_time = datetime.now().time()
    # current_time = re.findall(r'..:..:..', f"{accure_time}")[0]
    return render_template("alarm_map.html", news_data=news, alarm_data=alarm_data_1, time=current_time, \
                           onpage_map='true', onpage_analytics='false', onpage_help='false', onpage_us='false')

@app.route("/analytics")
def analytics():
    return render_template("analytics_map.html", danger_data=danger_data_1, danger_data_1=danger_data_1, danger_data_2=danger_data_2, \
                           onpage_map='false', onpage_analytics='true', onpage_help='false', onpage_us='false')

@app.route("/medical_help")
def medical_help():
    return render_template("medical_help.html", \
                           onpage_map='false', onpage_analytics='false', onpage_help='true', onpage_us='false')

@app.route("/about_us")
def about_us():
    return render_template("about_us.html", \
                           onpage_map='false', onpage_analytics='false', onpage_help='false', onpage_us='true')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# add_alarm(app, 'b', 'c', 'd', 'e', 'f')
# clear_alarm_table(app)

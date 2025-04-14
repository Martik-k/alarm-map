from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_migrate import Migrate
from models import db, process_alarm_data, clear_alarm_table, clear_shelling_table
from alarm import get_active_alerts
import getting_news
import time
import count_danger_level
from analytics import (  # change `your_module` to the actual Python filename without `.py`
    calculate_average_duration,
    count_alerts,
    calculate_alert_percentage,
    get_last_alert_time
)

app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///active_alerts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


# Ініціалізація глобальної змінної
alarm_data_1 = {}
news = ""
current_time  = datetime.now()
def get_data():
    global alarm_data_1
    global current_time
    global news
    while True:
        alarm_data_1 = get_active_alerts()
        news = getting_news.get_news()
        current_time = datetime.now()
        time.sleep(30)

def update_database():
    while True:
        with app.app_context():
            db.create_all()
            process_alarm_data(app, alarm_data_1, current_time)
            print('update')
        time.sleep(30)


danger_levels1 = {
    "Vinnytska": 0.0,
    "Volynska": 0.9,
    "Dnipropetrovska": 0.5,
    "Donetska": 1.0,
    "Zhytomyrska": 0.0,
    "Zakarpatska": 0.0,
    "Zaporizka": 0.5,
    "Ivano-Frankivska": 0.0,
    "Kyivska": 0.5,
    "Kirovohradska": 0.1,
    "Luhanska": 1.0,
    "Lvivska": 1.0,
    "Mykolaivska": 0.5,
    "Odeska": 0.5,
    "Poltavska": 0.0,
    "Rivnenska": 0.5,
    "Sumska": 1.0,
    "Ternopilska": 0.7,
    "Kharkivska": 1.0,
    "Khersonska": 0.5,
    "Khmelnytska": 0.1,
    "Cherkaska": 0.5,
    "Chernihivska": 0.25,
    "Chernivetska": 0.65,
    "Kyiv": 0.5,
    "Avtonomna Respublika Krym": 0.5
}

danger_levels2= {
    "Vinnytska": 0.0,
    "Volynska": 0.2,
    "Dnipropetrovska": 0.5,
    "Donetska": 1.0,
    "Zhytomyrska": 0.78,
    "Zakarpatska": 0.55,
    "Zaporizka": 0.5,
    "Ivano-Frankivska": 0.11,
    "Kyivska": 0.5,
    "Kirovohradska": 0.9,
    "Luhanska": 1.0,
    "Lvivska": 1.0,
    "Mykolaivska": 0.86,
    "Odeska": 0.5,
    "Poltavska": 0.2,
    "Rivnenska": 0.78,
    "Sumska": 1.0,
    "Ternopilska": 0.5,
    "Kharkivska": 1.0,
    "Khersonska": 0.65,
    "Khmelnytska": 0.0,
    "Cherkaska": 0.5,
    "Chernihivska": 0.31,
    "Chernivetska": 0.95,
    "Kyiv": 0.5,
    "Avtonomna Respublika Krym": 0.5
}

@app.route("/")
@app.route("/alarm_map")
def home():
    # accure_time = datetime.now().time()
    # current_time = re.findall(r'..:..:..', f"{accure_time}")[0]
    return render_template("alarm_map.html", news_data=news, alarm_data=alarm_data_1, time=current_time.strftime('%Y-%m-%d %H:%M:%S'), \
                           onpage_map='true', onpage_analytics='false', onpage_help='false', onpage_us='false')

@app.route("/analytics")
def analytics():
    min_alerts = 10
    max_alerts = 700
    min_shelling = 50
    max_shelling = 9000


    danger_data_1 = count_danger_level.count_color(danger_levels1)
    danger_data_2 = count_danger_level.count_color(danger_levels2)
    return render_template("analytics_map.html", danger_data=danger_data_1, danger_data_1=danger_data_1, danger_data_2=danger_data_2,  min_alerts =min_alerts, min_shelling = min_shelling, max_alerts= max_alerts, max_shelling=max_shelling,\
                           onpage_map='false', onpage_analytics='true', onpage_help='false', onpage_us='false')

@app.route("/medical_help")
def medical_help():
    return render_template("medical_help.html", \
                           onpage_map='false', onpage_analytics='false', onpage_help='true', onpage_us='false')

@app.route("/about_us")
def about_us():
    return render_template("about_us.html", \
                           onpage_map='false', onpage_analytics='false', onpage_help='false', onpage_us='true')

@app.errorhandler(404)
def not_found_error(error):
    return render_template("error_404.html"), "404"

@app.route('/api/alert-data', methods=['GET'])
def get_alert_data():
    region = request.args.get('region')
    month = int(request.args.get('month'))
    year = int(request.args.get('year'))

    region = region.replace("_", " ")
    file_path = 'history_alerts.json'  # adjust path if needed

    avg_duration = calculate_average_duration(region, month, year, file_path)
    count = count_alerts(region, month, year, file_path)
    percent = calculate_alert_percentage(region, month, year, file_path)
    last_alert = get_last_alert_time(region, file_path)

    return jsonify({
        'average_duration': avg_duration,
        'alert_count': count,
        'alert_percentage': round(percent, 2),
        'last_alert': last_alert
    })

if __name__ == "__main__":
    app.run(debug=True)

# add_alarm(app, 'b', 'c', 'd', 'e', 'f')
# clear_alarm_table(app)

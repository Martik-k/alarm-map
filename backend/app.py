from datetime import datetime
from models import db, init_db
from flask import Flask, render_template, request, jsonify
from models import db, init_db, add_alarm, clear_alarm_table
import re
import alarm
import getting_news
import time

from analytics import (  # change `your_module` to the actual Python filename without `.py`
    calculate_average_duration,
    count_alerts,
    calculate_alert_percentage,
    get_last_alert_time,
    plot_alert_durations_base64
)

app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///active_alerts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)

# Ініціалізація глобальної змінної
alarm_data_1 = {}
news = ""
current_time  = "00:00:00"
def get_data():
    global alarm_data_1
    global current_time 
    global news
    while True:
        alarm_data_1 = alarm.get_active_alerts()
        accure_time = datetime.now().time()
        news = getting_news.get_news()
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
    "Lvivska": "danger",
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
    "Lvivska": "danger",
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

@app.errorhandler(404)
def not_found_error(error):
    return render_template("error_404.html"), "404"


@app.route('/api/alert-data', methods=['GET'])
def get_alert_data():
    region = request.args.get('region')
    range_prop = request.args.get('range')

    print(range_prop)
    region = region.replace("_", " ")
    file_path = 'history_alerts.json'  # adjust path if needed

    try:
        avg_duration = calculate_average_duration(region, range_prop, file_path)
        count = count_alerts(region, range_prop, file_path)
        percent = calculate_alert_percentage(region, range_prop, file_path)
        last_alert = get_last_alert_time(region, file_path)
        image_base64 = plot_alert_durations_base64(region, range_prop, file_path)

        return jsonify({
            'average_duration': avg_duration,
            'alert_count': count,
            'alert_percentage': round(percent, 2),
            'last_alert': last_alert,
            'imageBase64': image_base64
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# add_alarm(app, 'b', 'c', 'd', 'e', 'f')
# clear_alarm_table(app)

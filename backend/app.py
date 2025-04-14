from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_migrate import Migrate
from models import db, process_alarm_data, process_shelling_data
from alarm import get_active_alerts
import getting_news
import time
import count_danger_level
import scratch_tg_shelling
import timeframe_analitiks
import update_tg_scretch
import asyncio
import threading

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
with scratch_tg_shelling.client:
    messege =  scratch_tg_shelling.client.loop.run_until_complete( scratch_tg_shelling.fetch_messages())
    filtert_data, last_data = timeframe_analitiks.extract_shelling_info(messege)
    process_shelling_data(app,filtert_data)



def start_async_shelling(last_data):
    asyncio.run(_async_get_shelling(last_data))

async def _async_get_shelling(last_data):
    data = await update_tg_scretch.update_messages(last_data)
    filtert_data, last_data = timeframe_analitiks.extract_shelling_info(data)
    last_data += ':00'

    print(filtert_data, last_data)
    process_shelling_data(app, filtert_data)
    
threading.Thread(target=start_async_shelling, args=(last_data,)).start()
        

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
    range_prop = request.args.get('range')

    print(region, range_prop)
    file_path = 'history_alerts.json'
    

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
    app.run(debug=True)

# add_alarm(app, 'b', 'c', 'd', 'e', 'f')
# clear_alarm_table(app)

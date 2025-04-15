from flask import Blueprint, render_template, request, jsonify, current_app
from utils import analytics_tools
from utils.danger_levels import danger_levels1, danger_levels2
from datetime import datetime
from utils import count_danger_level

main = Blueprint('main', __name__)

current_time = datetime.now()
news_data = ""

@main.route("/")
@main.route("/alarm_map")
def home():
    alarm_data = current_app.config.get('ALARM_DATA', {})
    return render_template("alarm_map.html", news_data=news_data, alarm_data=alarm_data,
                           time=current_time.strftime('%Y-%m-%d %H:%M:%S'),
                           onpage_map='true', onpage_analytics='false', onpage_help='false', onpage_us='false')

@main.route("/analytics")
def analytics():
    danger_data_1 = count_danger_level.count_color(danger_levels1)
    danger_data_2 = count_danger_level.count_color(danger_levels2)
    return render_template("analytics_map.html", danger_data=danger_data_1,
                           danger_data_1=danger_data_1, danger_data_2=danger_data_2,
                           min_alerts=10, min_shelling=50, max_alerts=700, max_shelling=9000,
                           onpage_map='false', onpage_analytics='true', onpage_help='false', onpage_us='false')

@main.route("/medical_help")
def medical_help():
    return render_template("medical_help.html", onpage_map='false', onpage_analytics='false', onpage_help='true', onpage_us='false')

@main.route("/about_us")
def about_us():
    return render_template("about_us.html", onpage_map='false', onpage_analytics='false', onpage_help='false', onpage_us='true')

@main.errorhandler(404)
def not_found_error(error):
    return render_template("error_404.html"), 404

@main.route('/api/alert-data', methods=['GET'])
def get_alert_data():
    region = request.args.get('region')
    range_prop = request.args.get('range')
    file_path = 'history_alerts.json'

    try:
        avg_duration = analytics_tools.calculate_average_duration(region, range_prop, file_path)
        count = analytics_tools.count_alerts(region, range_prop, file_path)
        percent = analytics_tools.calculate_alert_percentage(region, range_prop, file_path)
        last_alert = analytics_tools.get_last_alert_time(region, file_path)
        image_base64 = analytics_tools.plot_alert_durations_base64(region, range_prop, file_path)

        return jsonify({
            'average_duration': avg_duration,
            'alert_count': count,
            'alert_percentage': round(percent, 2),
            'last_alert': last_alert,
            'imageBase64': image_base64
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
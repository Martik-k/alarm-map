"""
Routes.
"""

from datetime import datetime, timezone
from flask import Blueprint, render_template, request, jsonify, current_app

TRANSLATE_LOCATION = {
    "Вінницька область": "Vinnytska",
    "Волинська область": "Volynska",
    "Дніпропетровська область": "Dnipropetrovska",
    "Донецька область": "Donetska",
    "Житомирська область": "Zhytomyrska",
    "Закарпатська область": "Zakarpatska",
    "Запорізька область": "Zaporizka",
    "Івано-Франківська область": "Ivano-Frankivska",
    "Київська область": "Kyivska",
    "Кіровоградська область": "Kirovohradska",
    "Луганська область": "Luhanska",
    "Львівська область": "Lvivska",
    "Миколаївська область": "Mykolaivska",
    "Одеська область": "Odeska",
    "Полтавська область": "Poltavska",
    "Рівненська область": "Rivnenska",
    "Сумська область": "Sumska",
    "Тернопільська область": "Ternopilska",
    "Харківська область": "Kharkivska",
    "Херсонська область": "Khersonska",
    "Хмельницька область": "Khmelnytska",
    "Черкаська область": "Cherkaska",
    "Чернігівська область": "Chernihivska",
    "Чернівецька область": "Chernivetska",
    "м. Київ": "Kyiv",
    "Автономна Республіка Крим": "Avtonomna Respublika Krym"
}


def get_kyiv_time():
    now = datetime.now(timezone.utc)
    dt_local = now.astimezone()
    dt_naive_local = dt_local.replace(tzinfo=None)
    return dt_naive_local


main = Blueprint('main', __name__)

@main.route("/")
@main.route("/alarm_map")
def home():
    """
    Renders the 'alarm_map.html' template.

    This function handles requests to the root URL ("/") and the "/alarm_map" URL.
    It passes data to the template for display, including news, alarm data, the current time,
    and flags indicating the active page.
    """
    return render_template("alarm_map.html", news_data=current_app.updater_alarms_news.news_data,
                           alarm_data=current_app.updater_alarms_news.alerts_data,
                           time=get_kyiv_time().strftime('%Y-%m-%d %H:%M:%S'),
                           onpage_map='true', onpage_analytics='false', onpage_help='false',
                           onpage_us='false')

@main.route("/analytics")
def analytics():
    """
    Renders the 'analytics_map.html' template.

    This function handles requests to the "/analytics" URL.  It passes danger level data
    and minimum/maximum values for alerts and shellings to the template.
    """
    return render_template("analytics_map.html",
                           danger_data=current_app.updater_analytics.alarms_colors,
                           danger_data_1=current_app.updater_analytics.alarms_colors,
                           danger_data_2=current_app.updater_analytics.shellings_colors,
                           min_alerts = current_app.updater_analytics.alarms_min,
                           min_shelling = current_app.updater_analytics.shellings_min,
                           max_alerts= current_app.updater_analytics.alarms_max,
                           max_shelling=current_app.updater_analytics.shellings_max,
                           onpage_map='false', onpage_analytics='true', onpage_help='false',
                           onpage_us='false')

@main.route("/medical_help")
def medical_help():
    """
    Renders the 'medical_help.html' template.
    """
    return render_template("medical_help.html",
                           onpage_map='false', onpage_analytics='false', onpage_help='true',
                           onpage_us='false')

@main.route("/about_us")
def about_us():
    """
    Renders the 'about_us.html' template.
    """
    return render_template("about_us.html",
                           onpage_map='false', onpage_analytics='false', onpage_help='false',
                           onpage_us='true')


@main.route('/api/alert-data', methods=['GET'])
def get_alert_data():
    """
    Handles requests to the '/api/alert-data' endpoint.

    This function retrieves alert data for a specified region and time range.
    It calculates and returns average duration, alert count, percentage, last alert time,
    and a base64 encoded image for a plot of the data.

    Returns:
        JSON: A JSON object containing the alert data, or an error message if an exception occurs.
              The JSON object has the following structure on success:
              {
                  'average_duration': float,
                  'alert_count': int,
                  'alert_percentage': float,
                  'last_alert': str,
                  'imageBase64': str (base64 encoded image)
              }
        HTTP 500: If an error occurs during the data retrieval or calculation process.
    """
    region = TRANSLATE_LOCATION[request.args.get('region')]
    range_prop = request.args.get('range')

    try:
        avg_duration = current_app.updater_analytics.avg_duration_dict[range_prop][region]
        count = current_app.updater_analytics.count_dict[range_prop][region]
        percent = current_app.updater_analytics.percent_dict[range_prop][region]
        last_alert = current_app.updater_analytics.last_alert_dict[range_prop][region]
        image_base64 = current_app.updater_analytics.image_base64_dict[range_prop][region]
        return jsonify({
            'average_duration': avg_duration,
            'alert_count': count,
            'alert_percentage': round(percent, 2),
            'last_alert': last_alert,
            'imageBase64': image_base64
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 500

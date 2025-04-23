"""
Run server.
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta
from time import sleep
from threading import Thread
from waitress import serve
from app import create_app
from flask import Flask
from database.db_utils.alarms_table import clear_alarms_table, add_alarm
from database.db_utils.shellings_table import clear_shellings_table
from scratching.alarms_month_scratching import get_month_alerts
from app.tasks import UpdateAnalytics

app: Flask = create_app()

def start_flask():
    """
    Starts the Flask application using the Waitress WSGI server.

    This function is intended to be run in a separate thread.  It calls
    `serve` with the Flask application instance (`app`), binding to
    all available network interfaces (0.0.0.0) on port 8000.
    """
    serve(app, host='0.0.0.0', port=8000)


if __name__ == "__main__":
    clear_shellings_table(app)

    # month_alerts = get_month_alerts()
    # for start, finish, location, is_active in month_alerts:
    #     add_alarm(app, start, finish, location, is_active)

    UpdateAnalytics.start_time = datetime.now() - relativedelta(months=1)
    # sleep(30)

    alarms_news_thread = Thread(target=app.updater_alarms_news.update_active_alerts_and_news,
                                daemon=True)
    alarms_news_thread.start()

    shellings_thread = Thread(target=app.updater_shellings.update_active_shellings, daemon=True)
    shellings_thread.start()

    analytics_tread = Thread(target=app.updater_analytics.update_active_analytics, daemon=True)
    analytics_tread.start()

    serve(app, host='0.0.0.0', port=8000)
    # asyncio.run(start_background_tasks())

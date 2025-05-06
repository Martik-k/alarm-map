"""
Run server.
"""

import time
from threading import Thread
from dateutil.relativedelta import relativedelta
from waitress import serve
from flask import Flask
from database.db_utils.shellings_table import clear_shellings_table
from app import create_app
from app.tasks import UpdateAnalytics
from app.const import get_kyiv_time
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

    UpdateAnalytics.start_time = get_kyiv_time() - relativedelta(months=1)

    alarms_news_thread = Thread(target=app.updater_alarms_news.update_active_alerts_and_news,
                                daemon=True)
    alarms_news_thread.start()

    shellings_thread = Thread(target=app.updater_shellings.update_active_shellings, daemon=True)
    shellings_thread.start()

    time.sleep(200)

    analytics_tread = Thread(target=app.updater_analytics.update_active_analytics, daemon=True)
    analytics_tread.start()

    serve(app, host='0.0.0.0', port=8000)
    # asyncio.run(start_background_tasks())

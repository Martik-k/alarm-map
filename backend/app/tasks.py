import time
from scratching.news_scratching import get_news
from scratching.alarm_scratching import get_active_alerts
from scratching.shellings_scratching import get_shellings
from database.db_utils.alarms_table import process_alarm_data, create_alarms_dictionary
from database.db_utils.shellings_table import process_shelling_data, create_shellings_dictionary
from analytics_utils.filter_shellings import filter_shelling_info
from analytics_utils.count_danger_level import count_percent_danger
from analytics_utils.analytics import (calculate_average_duration, count_alerts, calculate_alert_percentage,
                                       get_last_alert_time, plot_analytics_from_dict)
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def get_kyiv_time():
    now_kyiv = datetime.now(ZoneInfo("Europe/Kyiv"))
    return now_kyiv.replace(tzinfo=None)


class UpdateActiveAlertsNews:
    """
    A class responsible for periodically fetching and processing active alerts and news.
    """
    def __init__(self, app):
        """
        Initializes the Update_active_alerts_news instance.

        Args:
            app (Flask): The Flask application instance.
        """
        self.app = app
        self.alerts_data = {}
        self.news_data = {}
        self.update_time = datetime(2022, 1, 1, 0, 0, 0)


    def update_active_alerts_and_news(self):
        """
        Continuously fetches active alerts and news, processes the alert data,
        and updates the internal news data. It sleeps for 30 seconds after each update.
        It also initializes the global start time for analytics if it hasn't been set.
        """
        while True:
            self.alerts_data = get_active_alerts()
            # if UpdateAnalytics.start_time == datetime(2022, 1, 1, 0, 0, 0):
            #     UpdateAnalytics.start_time = datetime.now()
            process_alarm_data(self.app, self.alerts_data, get_kyiv_time())
            self.news_data = get_news()
            print('Alarms and news updated')
            time.sleep(30)


class UpdateActiveShellings:
    """
    A class responsible for periodically fetching and processing shelling data.
    """
    def __init__(self, app):
        """
        Initializes the Update_active_shellings instance.

        Args:
            app (Flask): The Flask application instance.
        """
        self.app = app
        self.last_data = datetime.strptime("2025-04-17 10:00:00", "%Y-%m-%d %H:%M:%S")
        self.now = None

    def update_active_shellings(self):
        """
        Continuously fetches shelling data since the last update, filters it,
        processes it, and updates the last fetched timestamp. It sleeps for 30 seconds
        after each update.
        """
        while True:
            self.now = get_kyiv_time()
            if self.now.hour == 1 and self.now.minute == 55:
                # process_shelling_data(active_shellings, current_time)
                data = get_shellings(self.last_data)
                shellings_data = filter_shelling_info(data)
                process_shelling_data(self.app, shellings_data)
                self.last_data = get_kyiv_time
                print('Shellings updated')
            time.sleep(30)


class UpdateAnalytics:
    """
    A class responsible for periodically calculating and storing various analytics
    related to alarms and shellings.
    """
    start_time = datetime(2022, 1, 1, 0, 0, 0)
    def __init__(self, app):
        """
        Initializes the Update_analytics instance.

        Args:
            app (Flask): The Flask application instance.
        """
        self.app = app
        self.now = None
        self.last_data = datetime.strptime("2025-04-17 10:00:00", "%Y-%m-%d %H:%M:%S")
        self.shellings_min = 0
        self.shellings_max = 0
        self.shellings_colors = {}
        self.alarms_min = 0
        self.alarms_max = 0
        self.alarms_colors = {}
        self.avg_duration_dict = {'week': {}, 'month': {}, 'year': {}}
        self.count_dict = {'week': {}, 'month': {}, 'year': {}}
        self.percent_dict = {'week': {}, 'month': {}, 'year': {}}
        self.last_alert_dict = {'week': {}, 'month': {}, 'year': {}}
        self.image_base64_dict = {'week': {}, 'month': {}, 'year': {}}


    def update_active_analytics(self):
        """
        Continuously updates various analytics data related to shellings and alarms.
        It fetches shelling data, calculates danger levels based on shelling counts,
        fetches alarm data, calculates average duration, alert counts, alert percentages,
        last alert times, and potentially generates plots for different time ranges
        (week, month, year). It sleeps for 60 seconds after each update.
        """
        while True:
            self.now = get_kyiv_time()
            if self.now.hour == 1 and self.now.minute == 59:
                shellings_month_data = create_shellings_dictionary(self.app)
                self.shellings_max = max(shellings_month_data.values())
                self.shellings_min = min(shellings_month_data.values())
                self.shellings_colors = \
                    count_percent_danger(shellings_month_data)

                alarms_dictionary, starts_dictionary = create_alarms_dictionary(self.app, UpdateAnalytics.start_time)

                alarms_month_count_data = {location: lst[0]
                                    for location, lst in alarms_dictionary['month'].items()}
                self.alarms_max = max(alarms_month_count_data.values())
                self.alarms_min = min(alarms_month_count_data.values())
                alarms_month_data = {location: lst[1]
                                    for location, lst in alarms_dictionary['month'].items()}
                self.alarms_colors = \
                    count_percent_danger(alarms_month_data)

                for time_range in ['week', 'month', 'year']:
                    for region, _ in alarms_dictionary[time_range].items():
                        self.avg_duration_dict[time_range][region] = \
                            calculate_average_duration(alarms_dictionary[time_range][region])
                        self.count_dict[time_range][region] = \
                            count_alerts(alarms_dictionary[time_range][region])
                        self.percent_dict[time_range][region] = \
                            calculate_alert_percentage(time_range,
                                                    alarms_dictionary[time_range][region],
                                                    UpdateAnalytics.start_time, starts_dictionary)
                        self.last_alert_dict[time_range][region] = \
                            get_last_alert_time(alarms_dictionary[time_range][region])
                        self.image_base64_dict[time_range][region] = \
                        plot_analytics_from_dict(alarms_dictionary, time_range, region, UpdateAnalytics.start_time)
                print('Analytics updated')
            time.sleep(30)

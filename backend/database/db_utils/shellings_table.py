from ..models import db, Shelling
from datetime import datetime, timezone
from copy import deepcopy

LOCATIONS_SHELLING_COUNT_DURATION = {
    "Vinnytska": 0,
    "Volynska": 0,
    "Dnipropetrovska": 0,
    "Donetska": 0,
    "Zhytomyrska": 0,
    "Zakarpatska": 0,
    "Zaporizka": 0,
    "Ivano-Frankivska": 0,
    "Kyivska": 0,
    "Kirovohradska": 0,
    "Luhanska": 0,
    "Lvivska": 0,
    "Mykolaivska": 0,
    "Odeska": 0,
    "Poltavska": 0,
    "Rivnenska": 0,
    "Sumska": 0,
    "Ternopilska": 0,
    "Kharkivska": 0,
    "Khersonska": 0,
    "Khmelnytska": 0,
    "Cherkaska": 0,
    "Chernihivska": 0,
    "Chernivetska": 0,
    "Kyiv": 0,
    "Avtonomna Respublika Krym": 0
}


def get_kyiv_time():
    now = datetime.now(timezone.utc)
    dt_local = now.astimezone()
    dt_naive_local = dt_local.replace(tzinfo=None)
    return dt_naive_local


def clear_shellings_table(app):
    """
    Clears all records from the Shelling table in the database.

    Args:
        app (Flask): The Flask application instance.
    """
    with app.app_context():
        db.session.query(Shelling).delete()
        db.session.commit()


def process_shelling_data(app, shelling_data: list[dict[str, str]]):
    """
    Processes a list of shelling data dictionaries and adds them to the database.

    Args:
        app (Flask): The Flask application instance.
        shelling_data (list[dict[str, str]]): A list of dictionaries, where each
                                               dictionary contains 'time' (str) and
                                               'city' (str) keys representing a shelling incident.
    """
    with app.app_context():
        for shelling in shelling_data:
            new_shelling = Shelling(time=shelling['time'], location=shelling['city'])
            db.session.add(new_shelling)
            db.session.commit()


def create_shellings_dictionary(app):
    """
    Creates a dictionary containing the total count of shellings for each location
    within the current month.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        dict[str, int]: A dictionary where keys are location names (str) and
                       values are the total number of shelling incidents in that
                       location for the current month (int).
    """
    with app.app_context():
        start_period = get_kyiv_time().replace(day=1)
        shellings = Shelling.query.filter(Shelling.time > start_period).all()
        total_count_shellingws = deepcopy(LOCATIONS_SHELLING_COUNT_DURATION)
        for shelling in shellings:
            total_count_shellingws[shelling.location] += 1
        total_count_shellingws['Kyiv'] = total_count_shellingws['Kyivska']
    return total_count_shellingws

"""
Filter shellings.
"""

def filter_shelling_info(shelling: list):
    """
    Filters a list of shelling incident data to identify relevant entries 
    and extract key information.

    This function processes a list of dictionaries, where each dictionary 
    represents a shelling incident and contains a 'message' key with a text 
    description of the incident.  It filters the entries based on the 
    presence of predefined keywords related to alerts and regions.

    Args:
        shelling (list): A list of dictionaries, where each dictionary contains
                        a 'message' key (string) describing the shelling incident
                        and a 'date' key (string) with the datetime of the event.

    Returns:
        list: A list of dictionaries, where each dictionary contains the extracted
              'time' (datetime object) and 'city' (string, representing the region)
              information from the filtered shelling incidents.  Returns an empty list
              if no relevant shelling incidents are found.
              The 'time' is converted to a datetime object from the original string.
    """
    alert_keywords = ['вибух', 'вибухи', 'удар', 'удари', 'загроза', 'ракета', 
                      'дрон', 'shahed', '💥', '🚀', '✈️']

    regions_keywords = {
        "Vinnytska": ["вінниц", "вінницьк"],
        "Volynska": ["волин", "луцьк"],
        "Dnipropetrovska": ["дніпро", "дніпропетров", "павлоград", "кривий ріг"],
        "Donetska": ["донецьк", "краматорськ", "маріуполь", "бахмут", "слов'янськ"],
        "Zhytomyrska": ["житомир"],
        "Zakarpatska": ["ужгород", "закарпат"],
        "Zaporizka": ["запоріж", "запорізьк"],
        "Ivano-Frankivska": ["івано-франків", "франківськ"],
        "Kyivska": ["київська"],
        "Kirovohradska": ["кіровоград", "кропивницьк"],
        "Luhanska": ["луганськ", "сєвєродонецьк"],
        "Lvivska": ["львів", "львівськ"],
        "Mykolaivska": ["миколаїв"],
        "Odeska": ["одеса", "одеськ"],
        "Poltavska": ["полтава", "полтавськ", "кременчук"],
        "Rivnenska": ["рівне", "рівненськ"],
        "Sumska": ["сум", "сумськ"],
        "Ternopilska": ["терноп", "тернопільськ"],
        "Kharkivska": ["харків", "харківськ"],
        "Khersonska": ["херсон"],
        "Khmelnytska": ["хмельницьк"],
        "Cherkaska": ["черкас", "золотоноша", "черкащин"],
        "Chernivetska": ["чернівц", "буковин"],
        "Chernihivska": ["чернігів"],
        "Kyiv": ["м. київ", "київ"],
        "Avtonomna Respublika Krym": ["крим", "симферополь", "ялта"],
    }

    result = []

    for entry in shelling:
        msg = entry.get('message', '').lower()
        datetime_message = entry.get('date', '')
        if not msg or not datetime_message:
            continue

        if any(keyword in msg for keyword in alert_keywords):
            for region, keywords in regions_keywords.items():
                if any(k in msg for k in keywords):
                    result.append({
                        "time": datetime_message,
                        "city": region
                    })

    # Повертаємо last_datetime як об'єкт datetime
    return result

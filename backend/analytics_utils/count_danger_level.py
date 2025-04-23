"""
Count danger level.
"""

NOTDANGER = [168, 180, 128]
DANGER = [192, 71, 43]

DELTA_R = DANGER[0] - NOTDANGER[0]
DELTA_G = DANGER[1] - NOTDANGER[1]
DELTA_B = DANGER[2] - NOTDANGER[2]

def find_color(coefficient):
    r = NOTDANGER[0] + coefficient * DELTA_R
    g = NOTDANGER[1] + coefficient * DELTA_G
    b = NOTDANGER[2] + coefficient * DELTA_B
    return f"rgb({int(round(r))}, {int(round(g))}, {int(round(b))})"

def count_color(cites):
    """
    Calculates an RGB color string based on a given danger coefficient.
    The color interpolates between NOTDANGER and DANGER based on the coefficient.

    Args:
        coefficient (float): A value between 0 and 1 (inclusive) representing the
                             level of danger. 0 corresponds to NOTDANGER, and 1
                             corresponds to DANGER.

    Returns:
        str: An RGB color string in the format "rgb(r, g, b)".
    """
    danger_data = {}
    for region, level in cites.items():
        danger_data[region] = find_color(level)
    return danger_data


def count_percent_danger(dictuanary_num):
    """
    Assigns a danger color to each region based on its danger level coefficient.

    Args:
        cites (dict[str, float]): A dictionary where keys are region names (str)
                                  and values are their corresponding danger level
                                  coefficients (float between 0 and 1).

    Returns:
        dict[str, str]: A dictionary where keys are region names (str) and values
                         are their corresponding RGB color strings representing
                         the danger level.
    """
    max_num = max(dictuanary_num.values())
    if max_num == 0:
        max_num = 1
    danger_levels = {
        region: round(count / max_num, 2) \
        for region, count in dictuanary_num.items()
    }
    return count_color(danger_levels)

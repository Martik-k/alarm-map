

notdanger = [168, 180, 128]
danger = [192, 71, 43]

d_r = danger[0] - notdanger[0]
d_g = danger[1] - notdanger[1]
d_b = danger[2] - notdanger[2]

def find_color(coefficient):
    r = notdanger[0] + coefficient * d_r
    g = notdanger[1] + coefficient * d_g
    b = notdanger[2] + coefficient * d_b
    return f"rgb({int(round(r))}, {int(round(g))}, {int(round(b))})"


# for i in range(11):
#     print(find_color(i*0.1))

def count_color(cites):
    danger_data = {}
    for region, level in cites.items():
        danger_data[region] = find_color(level)
    return danger_data



# danger_levels2= {
#     "Vinnytska": 0.0,
#     "Volynska": 1.0,
#     "Dnipropetrovska": 0.5,
#     "Donetska": 1.0,
#     "Zhytomyrska": 0.0,
#     "Zakarpatska": 0.0,
#     "Zaporizka": 0.5,
#     "Ivano-Frankivska": 0.0,
#     "Kyivska": 0.5,
#     "Kirovohradska": 0.0,
#     "Luhanska": 1.0,
#     "Lvivska": 1.0,
#     "Mykolaivska": 0.5,
#     "Odeska": 0.5,
#     "Poltavska": 0.0,
#     "Rivnenska": 0.5,
#     "Sumska": 1.0,
#     "Ternopilska": 0.5,
#     "Kharkivska": 1.0,
#     "Khersonska": 0.5,
#     "Khmelnytska": 0.0,
#     "Cherkaska": 0.5,
#     "Chernihivska": 0.0,
#     "Chernivetska": 0.5,
#     "Kyiv": 0.5,
#     "Avtonomna Respublika Krym": 0.5
# }

# print(danger_levels2)
# danger_data_2 = count_color(danger_levels2)
# print(danger_data_2)
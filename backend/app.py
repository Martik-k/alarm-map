from flask import Flask, render_template


app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend")


danger_data_1= {
    "Vinnytska": "notdanger",
    "Volynska": "danger",
    "Dnipropetrovska": "lessdanger",
    "Donetska": "danger",
    "Zhytomyrska": "notdanger",
    "Zakarpatska": "notdanger",
    "Zaporizka": "lessdanger",
    "Ivano-Frankivska": "notdanger",
    "Kyivska": "lessdanger",
    "Kirovohradska": "notdanger",
    "Luhanska": "danger",
    "Lvivska": "notdanger",
    "Mykolaivska": "lessdanger",
    "Odeska": "lessdanger",
    "Poltavska": "notdanger",
    "Rivnenska": "lessdanger",
    "Sumska": "danger",
    "Ternopilska": "lessdanger",
    "Kharkivska": "danger",
    "Khersonska": "lessdanger",
    "Khmelnytska": "notdanger",
    "Cherkaska": "lessdanger ",
    "Chernihivska": "notdanger",
    "Chernivetska": "lessdanger ",
    "Kyiv": "lessdanger",
    "Sevastopilska" : "lessdanger"
}
danger_data_2= {
    "Vinnytska": "notdanger",
    "Volynska": "danger",
    "Dnipropetrovska": "lessdanger",
    "Donetska": "danger",
    "Zhytomyrska": "notdanger",
    "Zakarpatska": "notdanger",
    "Zaporizka": "danger",
    "Ivano-Frankivska": "notdanger",
    "Kyivska": "lessdanger",
    "Kirovohradska": "notdanger",
    "Luhanska": "danger",
    "Lvivska": "notdanger",
    "Mykolaivska": "lessdanger",
    "Odeska": "lessdanger",
    "Poltavska": "notdanger",
    "Rivnenska": "danger",
    "Sumska": "danger",
    "Ternopilska": "lessdanger",
    "Kharkivska": "danger",
    "Khersonska": "lessdanger",
    "Khmelnytska": "notdanger",
    "Cherkaska": "lessdanger ",
    "Chernihivska": "ndanger",
    "Chernivetska": "lessdanger ",
    "Kyiv": "lessdanger",
    "Sevastopilska" : "lessdanger"
}

@app.route("/")
@app.route("/alarm_map")
def home():
    return render_template("alarm_map.html", danger_data=danger_data_1, danger_data_2 = danger_data_2)

@app.route("/analytics")
def analytics():
    return render_template("analytics_map.html", danger_data=danger_data_1, danger_data_2=danger_data_2)


@app.route("/about_us")
def about_us():
    return render_template("about_us.html")

@app.route("/medical_help")
def medical_help():
    return render_template("medical_help.html")


if __name__ == "__main__":
    app.run(debug=True)
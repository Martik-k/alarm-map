from datetime import datetime, timezone
from flask import Flask, render_template
import re


app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend")


alarm_data_1 = {
    "Vinnytska": "notalarm",
    "Volynska": "alarm",
    "Dnipropetrovska": "notalarm",
    "Donetska": "alarm",
    "Zhytomyrska": "notalarm",
    "Zakarpatska": "notalarm",
    "Zaporizka": "notalarm",
    "Ivano-Frankivska": "notalarm",
    "Kyivska": "notalarm",
    "Kirovohradska": "notalarm",
    "Luhanska": "alarm",
    "Lvivska": "notalarm",
    "Mykolaivska": "notalarm",
    "Odeska": "notalarm",
    "Poltavska": "notalarm",
    "Rivnenska": "notalarm",
    "Sumska": "alarm",
    "Ternopilska": "notalarm",
    "Kharkivska": "alarm",
    "Khersonska": "notalarm",
    "Khmelnytska": "notalarm",
    "Cherkaska": "notalarm",
    "Chernihivska": "notalarm",
    "Chernivetska": "notalarm",
    "Kyiv": "notalarm",
    "Avtonomna Respublika Krym": "notalarm"
}

alarm_data_2 = {
    "Vinnytska": "notalarm",
    "Volynska": "alarm",
    "Dnipropetrovska": "notalarm",
    "Donetska": "alarm",
    "Zhytomyrska": "notalarm",
    "Zakarpatska": "notalarm",
    "Zaporizka": "alarm",
    "Ivano-Frankivska": "notalarm",
    "Kyivska": "notalarm",
    "Kirovohradska": "notalarm",
    "Luhanska": "alarm",
    "Lvivska": "notalarm",
    "Mykolaivska": "notalarm",
    "Odeska": "notalarm",
    "Poltavska": "notalarm",
    "Rivnenska": "alarm",
    "Sumska": "alarm",
    "Ternopilska": "notalarm",
    "Kharkivska": "alarm",
    "Khersonska": "notalarm",
    "Khmelnytska": "notalarm",
    "Cherkaska": "notalarm",
    "Chernihivska": "notalarm",
    "Chernivetska": "notalarm",
    "Kyiv": "notalarm",
    "Avtonomna Respublika Krym": "notalarm"
}


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
    "Avtonomna Respublika Krym" : "lessdanger"
}


danger_data_2= {
    "Vinnytska": "notdanger",
    "Volynska": "danger",
    "Dnipropetrovska": "danger",
    "Donetska": "danger",
    "Zhytomyrska": "notdanger",
    "Zakarpatska": "danger",
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
    "Avtonomna Respublika Krym" : "lessdanger"
}


@app.route("/")
@app.route("/alarm_map")
def home():
    accure_time = datetime.now().time()
    time = re.findall(r'..:..:..', f"{accure_time}")[0]
    return render_template("alarm_map.html", alarm_data=alarm_data_1, alarm_data_2=alarm_data_2, time=time, \
                           onpage_map='true', onpage_analytics='false', onpage_help='false', onpage_us='false')

@app.route("/analytics")
def analytics():
    return render_template("analytics_map.html", danger_data=danger_data_1,danger_data_1=danger_data_1, danger_data_2=danger_data_2, \
                           onpage_map='false', onpage_analytics='true', onpage_help='false', onpage_us='false')

@app.route("/medical_help")
def medical_help():
    return render_template("medical_help.html", \
                           onpage_map='false', onpage_analytics='false', onpage_help='true', onpage_us='false')

@app.route("/about_us")
def about_us():
    return render_template("about_us.html", \
                           onpage_map='false', onpage_analytics='false', onpage_help='false', onpage_us='true')

if __name__ == "__main__":
    app.run(debug=True)

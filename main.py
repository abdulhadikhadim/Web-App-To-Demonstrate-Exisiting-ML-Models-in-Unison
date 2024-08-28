from flask import Flask, render_template, request, session, flash
from flask_session import Session
from starter import MongoFetcher
import json
import requests
from patient import Patient
from chronic import ChronicDiseasePred

API_URL = "http://172.16.101.167:5000/integrate"

app = Flask("__main__")
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "your_secret_key_here"
Session(app)

diagnosis = {}
patient1 = Patient()

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        session['PID'] = request.form['PID']
        session['PP'] = request.form['PP'] 
        
        mongo_fetcher = MongoFetcher()
        patient1.patient_ID = session.get("PID", '')
        patient1.patient_practice = session.get("PP", '')
        pat = mongo_fetcher.get_patients_from_mongo(patient1.patient_ID, patient1.patient_practice)
        patient1.data = json.loads(pat)
        
        if patient1.data == {}:
            print("Condition True")
            flash("Patient ID or Practice is Incorrect!")

        else:  
            keys = ["_id", "patientid", "practice"]
            patient1.clean_data(keys)
            return json.dumps(patient1.data)
            
    return render_template("index.html")


@app.route('/diagnose')
def diagnose():
    global diagnosis
    response = requests.post(API_URL, json = patient1.data)
    diagnosis = response.json()
    # print(diagnosis)
    # return render_template("response.html", diagnosis = diagnosis)

    return render_template('diagnose.html', data = patient1.data)

@app.route("/response")
def response_from_api():
    response = requests.post(API_URL, json = patient1.data)
    diagnosis = response.json()
    return render_template("response.html", diagnosis = diagnosis)

@app.route("/chronic")
def chronic_diagnosis():
    global diagnosis
    prediction = ChronicDiseasePred(diagnosis["chronic_diseases_response"])
    data, imp_features, risky = prediction.set_values()
    vector = data["CKD"]
    imp = imp_features["CKD"]
    risk = risky["CKD"]
    return render_template("chronic_disease.html", imp = imp, vector = vector, risk = risk, data = patient1.data)

@app.route("/medlabs")
def medlabs_response():
    return render_template("medlabs_response.html")

@app.route("/pattern")
def pattern_recognition():
    return render_template("pattern_recognition.html")

@app.route("/recommendation")
def recommendations():
    return render_template("Recommendation.html")
# @app.route('/get_patient_data')
# def get_patient_data():
#     PID = request.args.get('PID')
#     practice = request.args.get('PP')

#     mongo_fetcher = MongoFetcher()
#     pat = mongo_fetcher.get_patients_from_mongo(PID, practice)
#     data = json.loads(pat)
#     keys = ["_id", "patientid", "practice"]
#     for key in keys:
#         data.pop(key)

#     return json.dumps(data)


# @app.route('/save_input', methods=["POST"])
# def save_input():
#     session['PID'] = request.form['PID']
#     session['PP'] = request.form['PP']
#     return redirect(url_for("process"))

# @app.route('/save_input', methods=["POST"])
# def save_input():
#     session['PID'] = request.form['PID']
#     session['PP'] = request.form['PP']
    
#     mongo_fetcher = MongoFetcher()
#     PID = session.get("PID", '')
#     practice = session.get("PP", '')
#     pat = mongo_fetcher.get_patients_from_mongo(PID, practice)
#     data = json.loads(pat)
#     keys = ["_id", "patientid", "practice"]
#     for key in keys:
#         data.pop(key)
    
#     return json.dumps(data)



# @app.route("/process", methods=["GET"])
# def process():
#     mongo_fetcher = MongoFetcher()
#     PID = session.get("PID",'')
#     practice = session.get("PP",'')
#     print(PID, practice)
#     pat = mongo_fetcher.get_patients_from_mongo(PID, practice)
#     data = json.loads(pat)
#     keys = ["_id", "patientid", "practice"]
#     for key in keys:
#         data.pop(key)
#     return render_template("process.html", result = data)


if __name__ == '__main__':    
    app.run(debug=True, port=5000)


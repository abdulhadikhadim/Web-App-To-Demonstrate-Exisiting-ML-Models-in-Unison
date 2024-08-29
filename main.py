from flask import Flask, render_template, request, session, flash
from flask_session import Session
from starter import MongoFetcher
import json
import requests
from patient import Patient
from chronic import ChronicDiseasePred
from medlabs import MedLabPredictions
from recommendations import Recommendations

with open("static\disease_name_mapping.json", "r") as file:
    DISEASE_MAPPINGS = json.load(file)

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
    patient1.diagnosis_sorter()

    return render_template('diagnose.html', data = patient1.data)

@app.route("/response")
def response_from_api():
    response = requests.post(API_URL, json = patient1.data)
    diagnosis = response.json()
    return render_template("response.html", diagnosis = diagnosis)

@app.route("/chronic")
def chronic_diagnosis():
    global diagnosis
    global patient1
    prediction = ChronicDiseasePred(diagnosis["chronic_diseases_response"])
    patient1.chronic_pred = prediction
    names, prob, vector, imp_features, risky, rules = prediction.set_values()

    return render_template("chronic_disease.html", names=names, prob=prob, imp = imp_features, vector = vector, risk = risky, data=patient1.data, rules = rules)

@app.route("/medlabs")
def medlabs_response():
    global diagnosis
    global patient1
    med_data = diagnosis["medlabs_response"]
    med_preds = MedLabPredictions()
    patient1.medlab_pred = med_preds
    names, probs, feature_imp = med_preds.set_values(med_data)
    return render_template("medlabs_response.html", names=names, probs=probs, feature_imp=feature_imp)

@app.route("/pattern")
def pattern_recognition():
    return render_template("pattern_recognition.html")

@app.route("/recommendation")
def recommendations_response():
    global patient1
    global diagnosis
    filtered_names = patient1.recommendations_filter()
    recommendations_data = diagnosis["recommendations"]
    recommendations = Recommendations()
    names, procedures, surgeries, labs, lifestyle_changes = recommendations.set_values(filtered_names, recommendations_data)
    return render_template("Recommendation.html")

if __name__ == '__main__':    
    app.run(host="172.16.105.138",debug=True, port=5000)


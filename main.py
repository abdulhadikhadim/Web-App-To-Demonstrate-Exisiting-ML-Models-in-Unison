from flask import Flask, render_template, request, session, flash, render_template_string,redirect
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
    global patient1
   
    if request.method == "POST":
        print("in home")
        session['PID'] = request.form.get("PID", None)
        session['PP'] = request.form.get("PP", None)
       
        mongo_fetcher = MongoFetcher()
        patient1.patient_ID = session.get("PID", '')
        patient1.patient_practice = session.get("PP", '')
        pat = mongo_fetcher.get_patients_from_mongo(patient1.patient_ID, patient1.patient_practice)
        patient1.data = json.loads(pat)
        # print(patient1.data)
        if not patient1.data:
            flash("Patient ID or Practice is Incorrect!")
            return render_template("index.html")
 
        else:  
            keys = ["_id", "patientid", "practice"]
            patient1.clean_data(keys)
            return redirect("/diagnose")
               
    return render_template("index.html")

@app.route('/diagnose')
def diagnose():
    global diagnosis
    global patient1
    response = requests.post(API_URL, json = patient1.data)
    diagnosis = response.json()
    patient1.patient_data_collector(diagnosis)
    patient1.diagnosis_sorter()

    return render_template('diagnose.html', data = patient1.data)

@app.route("/response")
def response_from_api():
    response = requests.post(API_URL, json = patient1.data)
    diagnosis = response.json()
    return render_template("response.html", diagnosis = diagnosis)

# @app.route("/chronic")
# def chronic_diagnosis():
#     global diagnosis
#     global patient1
#     # prediction = ChronicDiseasePred(diagnosis["chronic_diseases_response"])
#     names, prob, vector, imp_features, risky, rules = patient1.get_chronic_pred()
#     return render_template("chronic_disease.html", names=names, prob=prob, imp = imp_features, vector = vector, risk = risky, data=patient1.data, rules = rules)

@app.route("/chronic")
def chronic_diagnosis():
    global diagnosis
    global patient1
    names, prob, vector, imp_features, risky, rules = patient1.get_chronic_pred()

    # Sort the names list based on the probability in descending order
    sorted_names = sorted(names, key=lambda x: prob[x], reverse=True)

    return render_template("chronic_disease.html", names=sorted_names, prob=prob, imp=imp_features, vector=vector, risk=risky, data=patient1.data, rules=rules)


@app.route("/medlabs")
def medlabs_response():
    global diagnosis
    global patient1
    names, probs, feature_imp = patient1.get_medlab_pred()
    return render_template("medlabs_response.html", names=names, probs=probs, feature_imp=feature_imp,data=patient1.data)

@app.route("/pattern")
def pattern_recognition():
    global patient1
    # print(patient1.chronic_pred.trajectory)
    fig = patient1.chronic_pred.sanky_plot_generator()
    plot_html = fig.to_html(full_html=False)
    return render_template("pattern_recognition.html", html = plot_html,data = patient1.data)

@app.route("/recommendation")
def recommendations_response():
    global patient1
    global diagnosis
    # names, probs, vector, imp_features, risky, rules = patient1.get_chronic_pred()
    names, procedures, surgeries, labs, lifestyle_changes = patient1.get_recommendations()
    full_names = [DISEASE_MAPPINGS.get(name, name) for name in names]
    return render_template("Recommendation.html", names=names, procedure=procedures, surgeries=surgeries, lab=labs, lifestyle=lifestyle_changes, data=patient1.data)

if __name__ == '__main__':    
    app.run(host = "172.16.105.134", debug=True, port=5000)


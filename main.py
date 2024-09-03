# from flask import Flask, render_template, request, session, flash, render_template_string,redirect
# from flask_session import Session
# from starter import MongoFetcher
# import json
# import requests
# from patient import Patient
# from chronic import ChronicPredictor
# from medlabs import MedLabPredictor
# from recommendations import Recommendations

# with open("static\disease_name_mapping.json", "r") as file:
#     DISEASE_MAPPINGS = json.load(file)

# API_URL = "http://172.16.101.167:5000/integrate"

# app = Flask("__main__")
# app.config["SESSION_TYPE"] = "filesystem"
# app.config["SECRET_KEY"] = "your_secret_key_here"
# Session(app)

# diagnosis = {}
# patient1 = Patient()


# @app.route('/', methods=["GET", "POST"])
# def home():
#     global patient1
#     patient1.reset_patient()
#     # print( patient1.patient_ID, patient1.patient_practice, patient1.chronic_pred, patient1.medlab_pred)
#     if request.method == "POST":
#         print("in home")
#         session['PID'] = request.form.get("PID", None)
#         session['PP'] = request.form.get("PP", None)
       
#         mongo_fetcher = MongoFetcher()
#         patient1.patient_ID = session.get("PID", '')
#         patient1.patient_practice = session.get("PP", '')
#         pat = mongo_fetcher.get_patients_from_mongo(patient1.patient_ID, patient1.patient_practice)
#         patient1.data = json.loads(pat)
#         print(patient1.data)
#         if not patient1.data:
#             flash("Patient ID or Practice is Incorrect!")
#             return render_template("index.html")
 
#         else:  
#             keys = ["_id", "patientid", "practice"]
#             patient1.clean_data(keys)
#             return redirect("/diagnose")
               
#     return render_template("index.html")

# @app.route('/diagnose')
# def diagnose():
#     if request.method == "GET":
#         global diagnosis
#         global patient1
#         # print( patient1.patient_ID, patient1.patient_practice, patient1.chronic_pred, patient1.medlab_pred)
#         response = requests.post(API_URL, json = patient1.data)
#         diagnosis = response.json()
#         patient1.patient_data_collector(diagnosis)
#         print(patient1.chronic_pred.names)
#         patient1.diagnosis_sorter()

#     return render_template('diagnose.html', data = patient1.data)


# @app.route("/chronic")
# def chronic_diagnosis():
#     global diagnosis
#     global patient1
#     names, prob, vector, imp_features, risky, rules = patient1.get_chronic_pred()

#     # Sort the names list based on the probability in descending order
#     sorted_names = sorted(names, key=lambda x: prob[x], reverse=True)
#     return render_template("chronic_disease.html", names=sorted_names, prob=prob, imp=imp_features, vector=vector, risk=risky, data=patient1.data, rules=rules)


# @app.route("/medlabs")
# def medlabs_response():
#     global diagnosis
#     global patient1
#     names, probs, feature_imp = patient1.get_medlab_pred()
#     return render_template("medlabs_response.html", names=names, probs=probs, feature_imp=feature_imp,data=patient1.data)


# @app.route("/pattern")
# def pattern_recognition():
#     global patient1
#     fig = patient1.chronic_pred.sankey_plot_generator()
#     plot_html = fig.to_html(full_html=False) if fig else None
#     return render_template("pattern_recognition.html", html=plot_html, data=patient1.data)


# @app.route("/recommendation")
# def recommendations_response():
#     global patient1
#     global diagnosis
#     names, procedures, surgeries, labs, lifestyle_changes = patient1.get_recommendations()
#     return render_template("Recommendation.html", names=names, procedure=procedures, surgeries=surgeries, lab=labs, lifestyle=lifestyle_changes, data=patient1.data)

# if __name__ == '__main__':    
#     app.run(host = "172.16.105.138", debug=True, port=5000)


from flask import Flask, render_template, request, session, flash, redirect
from flask_session import Session
import json
import requests
from patient import Patient
from starter import MongoFetcher
from chronic import ChronicPredictor
from medlabs import MedLabPredictor
from recommendations import Recommendations
from collections import defaultdict, namedtuple


with open("static\disease_name_mapping.json", "r") as file:
    DISEASE_MAPPINGS = json.load(file)

API_URL = "http://172.16.101.167:5000/integrate"

class FlaskApp:
    def __init__(self):
        self.app = Flask("__main__")
        self.app.config["SESSION_TYPE"] = "filesystem"
        self.app.config["SECRET_KEY"] = "your_secret_key_here"
        Session(self.app)
        
        self.diagnosis = {}
        self.patient1 = Patient()
        
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/', methods=["GET", "POST"])
        def home():
            return self.handle_home()

        @self.app.route('/diagnose')
        def diagnose():
            return self.handle_diagnose()

        @self.app.route("/chronic")
        def chronic_diagnosis():
            return self.handle_chronic_diagnosis()

        @self.app.route("/medlabs")
        def medlabs_response():
            return self.handle_medlabs_response()

        @self.app.route("/pattern")
        def pattern_recognition():
            return self.handle_pattern_recognition()

        @self.app.route("/recommendation")
        def recommendations_response():
            return self.handle_recommendations_response()

    def handle_home(self):
        self.patient1.reset_patient()
        if request.method == "POST":
            session['PID'] = request.form.get("PID", None)
            session['PP'] = request.form.get("PP", None)
            
            mongo_fetcher = MongoFetcher()
            self.patient1.patient_ID = session.get("PID", '')
            self.patient1.patient_practice = session.get("PP", '')
            pat = mongo_fetcher.get_patients_from_mongo(self.patient1.patient_ID, self.patient1.patient_practice)
            self.patient1.data = json.loads(pat)
            
            if not self.patient1.data:
                flash("Patient ID or Practice is Incorrect!")
                return render_template("index.html")
            else:
                keys = ["_id", "patientid", "practice"]
                self.patient1.clean_data(keys)
                return redirect("/diagnose")
               
        return render_template("index.html")

    def handle_diagnose(self):
        response = requests.post(API_URL, json=self.patient1.data)
        self.diagnosis = response.json()
        self.patient1.patient_data_collector(self.diagnosis)
        self.patient1.diagnosis_sorter()
        return render_template('diagnose.html', data=self.patient1.data)

    def handle_chronic_diagnosis(self):
        names, prob, vector, imp_features, risky, rules = self.patient1.get_chronic_pred()
        sorted_names = sorted(names, key=lambda x: prob[x], reverse=True)
        return render_template("chronic_disease.html", names=sorted_names, prob=prob, imp=imp_features, vector=vector, risk=risky, data=self.patient1.data, rules=rules)

    def handle_medlabs_response(self):
        names, probs, feature_imp = self.patient1.get_medlab_pred()
        return render_template("medlabs_response.html", names=names, probs=probs, feature_imp=feature_imp, data=self.patient1.data)

    def handle_pattern_recognition(self):
        fig = self.patient1.chronic_pred.sankey_plot_generator()
        plot_html = fig.to_html(full_html=False) if fig else None
        return render_template("pattern_recognition.html", html=plot_html, data=self.patient1.data)

    def handle_recommendations_response(self):
        names, procedures, surgeries, labs, lifestyle_changes = self.patient1.get_recommendations()
        return render_template("Recommendation.html", names=names, procedure=procedures, surgeries=surgeries, lab=labs, lifestyle=lifestyle_changes, data=self.patient1.data)


# @app.route("/recommendation")
# def recommendations_response():
#     global patient1
#     global diagnosis

#     # Retrieve the recommendations
#     names, procedures, surgeries, labs, lifestyle_changes = patient1.get_recommendations()

#     # Define a NamedTuple for storing grouped data
#     GroupedRecommendation = namedtuple('GroupedRecommendation', ['item', 'diseases'])

#     # Function to group recommendations by their items
#     def group_recommendations(names, recommendations_dict):
#         grouped = defaultdict(list)
#         for name in names:
#             if name != "Normal" and recommendations_dict.get(name):
#                 for item in recommendations_dict[name]:
#                     grouped[item].append(name)
#         return [GroupedRecommendation(item=k, diseases=', '.join(v)) for k, v in grouped.items()]

#     # Grouping the data
#     grouped_procedures = group_recommendations(names, procedures)
#     grouped_surgeries = group_recommendations(names, surgeries)
#     grouped_labs = group_recommendations(names, labs)
#     grouped_lifestyle_changes = group_recommendations(names, lifestyle_changes)

#     return render_template(
#         "Recommendation.html", 
#         grouped_procedures=grouped_procedures,
#         grouped_surgeries=grouped_surgeries,
#         grouped_labs=grouped_labs,
#         grouped_lifestyle_changes=grouped_lifestyle_changes,
#         data=patient1.data
#     )

if __name__ == '__main__':    
    app.run(host = "172.16.105.134", debug=True, port=5000)


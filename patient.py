from chronic import ChronicPredictor
from medlabs import MedLabPredictor
from recommendations import Recommendations
import json
from datetime import datetime


with open("static\disease_name_mapping.json", "r") as file:
    DISEASE_MAPPINGS = json.load(file)

class Patient:
    def __init__(self, patient_ID=0, patient_practice="", data=None, chronic_pred = None, medlab_pred = None, recommendations = None):
        self._patient_ID = patient_ID
        self._patient_practice = patient_practice
        self._data = data
        self.chronic_pred = chronic_pred
        self.medlab_pred = medlab_pred
        self.recommendations = recommendations

    @property
    def patient_ID(self):
        return self._patient_ID
    
    @patient_ID.setter
    def patient_ID(self, ID):
        self._patient_ID = ID 

    @patient_ID.deleter
    def patient_ID(self):
        del self._patient_ID

    @property
    def patient_practice(self):
        return self._patient_practice

    @patient_practice.setter
    def patient_practice(self, practice):
        self._patient_practice = practice
    
    @patient_practice.deleter
    def patient_practice(self):
        del self._patient_practice

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, val):
            self._data = val
    
    @data.deleter
    def data(self):
        del self._data

    def reset_patient(self):
        self.patient_ID = 0
        self.patient_practice = ""
        self.chronic_pred= None
        self.medlab_pred= None
        self.recommendations = None
        self.data=None

    def clean_data(self, keys):
        for key in keys:
            self._data.pop(key, None)
        return self._data
    
    def filter_recommendations(self):
        names = []
        for name in self.chronic_pred.names:
            if self.chronic_pred.prob[name]>=0.5:
                names.append(DISEASE_MAPPINGS[name])
        if "normal" in self.medlab_pred.names:
            names.append("Normal")
        else:
            for name in self.medlab_pred.names:
                if self.medlab_pred.prob[name]>=60:
                    names.append(DISEASE_MAPPINGS[name])
        return names   
    
    def sort_diagnosis(self):
        def parse_date(date_str):
            try: 
                return datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                return datetime.min

        sorted_diagnoses = sorted(self.data["Diagnoses"], key=lambda x: parse_date(x.get('Date', '')), reverse=True)
        self.data["Diagnoses"] = sorted_diagnoses

    def collect_patient_data(self, data):
        self.chronic_pred = ChronicPredictor()
        self.chronic_pred.set_values(data["chronic_diseases_response"])
        self.medlab_pred = MedLabPredictor()
        self.medlab_pred.set_values(data["medlabs_response"])
        self.recommendations = Recommendations()
        filtered_names = self.filter_recommendations()
        self.recommendations.set_values(filtered_names, data["recommendations"])
    
    def get_chronic_pred(self):
        return self.chronic_pred.names, self.chronic_pred.prob, self.chronic_pred.feature_vector, self.chronic_pred.imp_features, self.chronic_pred.risky_features, self.chronic_pred.top_pred_rules

    def get_medlab_pred(self):
        return self.medlab_pred.names, self.medlab_pred.prob, self.medlab_pred.imp_features, self.medlab_pred.confirmed_diag

    def get_recommendations(self):
        return self.recommendations.names, self.recommendations.procedures, self.recommendations.surgeries, self.recommendations.labs, self.recommendations.lifestyle_changes

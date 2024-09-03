from chronic import ChronicDiseasePred
from medlabs import MedLabPredictions
from recommendations import Recommendations
import json
from datetime import datetime


with open("static\disease_name_mapping.json", "r") as file:
    DISEASE_MAPPINGS = json.load(file)

class Patient:
    def __init__(self, patient_ID=0, patient_practice="", data={}, chronic_pred = None, medlab_pred = None, recommendations = None):
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

    @property
    def patient_practice(self):
        return self._patient_practice

    @patient_practice.setter
    def patient_practice(self, practice):
        self._patient_practice = practice

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, val):
        if val is not None:
            self._data = val
        else:
            pass

    def clean_data(self, keys):
        for key in keys:
            self._data.pop(key, None)
        return self._data
    
    def recommendations_filter(self):
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
    
    def diagnosis_sorter(self):
        def parse_date(date_str):
            try:
                return datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                return datetime.min

        sorted_diagnoses = sorted(self.data["Diagnoses"], key=lambda x: parse_date(x.get('Date', '')), reverse=True)
        self.data["Diagnoses"] = sorted_diagnoses

    def patient_data_collector(self, data):
        self.chronic_pred = ChronicDiseasePred()
        self.chronic_pred.set_values(data["chronic_diseases_response"])
        self.medlab_pred = MedLabPredictions()
        self.medlab_pred.set_values(data["medlabs_response"])
        self.recommendations = Recommendations()
        filtered_names = self.recommendations_filter()
        self.recommendations.set_values(filtered_names, data["recommendations"])
    
    def get_chronic_pred(self):
        return self.chronic_pred.names, self.chronic_pred.prob, self.chronic_pred.feature_vector, self.chronic_pred.important_features, self.chronic_pred.risky_features, self.chronic_pred.top_pred_rules

    def get_medlab_pred(self):
        return self.medlab_pred.names, self.medlab_pred.prob, self.medlab_pred.feature_imp

    def get_recommendations(self):
        return self.recommendations.names, self.recommendations.procedures, self.recommendations.surgeries, self.recommendations.labs, self.recommendations.lifestyle_changes

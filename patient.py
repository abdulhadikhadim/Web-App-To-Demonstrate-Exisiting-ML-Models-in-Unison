from chronic import ChronicDiseasePred
from medlabs import MedLabPredictions
from recommendations import Recommendations
import json

DISEASE_MAPPINGS = json.load("static\disease_name_mapping.json")

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
            if self.chronic_pred.prob>=0.5:
                name.append(DISEASE_MAPPINGS[name])
        return names   


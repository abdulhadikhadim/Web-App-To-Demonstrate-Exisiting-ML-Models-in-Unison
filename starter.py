from pymongo import MongoClient
import json

class MongoFetcher:
    def __init__(self):
        self.client = MongoClient('mongodb://172.16.103.206:27017/')
        # self.db = self.client['Patients_for_API']
        self.db = self.client['Patients_for_API']
        
        self.collection = self.db['PatientData']

    def get_patients_from_mongo(self, patientid, practice):
        """Fetches patient data from local mongo dump
        This is for demo application"""

        document = self.collection.find_one({"patientid": patientid, "practice": practice})  # Replace with your query
        pretty_json = json.dumps(document, indent=4, sort_keys=False, default=str)
        # print(pretty_json)
        return pretty_json


## Example list of patientid and practice pairs

# patient_practice_pairs = [
#     {'patientid': '60555', 'practice': 'AMERICAN PHYSICIANS FOUNDATION'},
#     {'patientid': '54418', 'practice': 'AMG Medical Group'},
#     {'patientid': '7684', 'practice': 'Advanced Integrative Medicine'},
#     {'patientid': '19501', 'practice': 'Ardent Family Care'},
# ]
# get_patient = MongoFetcher()
# print(get_patient.get_patients_from_mongo)
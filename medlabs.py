class MedLabPredictions:
    def __init__(self,disease_names=[], prob={}, feature_imp={}):
        self.disease_names = disease_names
        self.prob = prob
        self.feature_imp = feature_imp
    
    def set_values(self, data):
        for disease in data["likely_diag"]:
            name = disease["disease_name"]
            if name not in self.disease_names:
                self.disease_names.append(disease["disease_name"])
                self.prob[name] = disease["probability"]
                self.feature_imp[name] = disease["feature_importances"]
        return self.disease_names, self.prob, self.feature_imp


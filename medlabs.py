class MedLabPredictions:
    def __init__(self,names=[], prob={}, feature_imp={}):
        self.names = names
        self.prob = prob
        self.feature_imp = feature_imp
    
    def set_values(self, data):
        for disease in data["likeky_diage"]:
            name = disease["disease_name"]
            if name not in self.names:
                self.names.append(disease["disease_name"])
                self.prob[name] = disease["probability"]
                self.feature_imp[name] = disease["feature_importances"]
        return self.names, self.prob, self.feature_imp


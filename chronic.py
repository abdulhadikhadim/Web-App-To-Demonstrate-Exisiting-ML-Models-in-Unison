class ChronicDiseasePred:
    def __init__(self, chronic_data, feature_vector={}, important_features={}, risky_features={}, names=[], macro_rules = {}, top_pred_rules = {}, prob = {}):
        self.chronic_data = chronic_data
        self.names = names
        self.prob = prob
        self.feature_vector = feature_vector
        self.important_features = important_features
        self.risky_features = risky_features
        self.macro_rules = macro_rules
        self.top_pred_rules = top_pred_rules


    def set_values(self):
        for diseases in self.chronic_data["Content"]["DiseasePredictions"]:
            if diseases["Disease"] not in self.names:
                self.names.append(diseases["Disease"])
                self.prob[diseases["Disease"]] = diseases["ModelsProbabilities"]["12_months"]
                self.feature_vector[diseases["Disease"]] = diseases["FeatureVector"]
                self.risky_features[diseases["Disease"]] = diseases["RiskyFeatures"]
                self.important_features[diseases["Disease"]] = diseases["AllImportantFeatures"]
                self.top_pred_rules[diseases["Disease"]] = diseases["TopPredictionRules"]
        return self.names, self.prob, self.feature_vector, self.important_features, self.risky_features, self.top_pred_rules


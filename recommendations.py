import json
with open("static/recommendations.json", "r") as file:
    DISEASE_RECOMMENDATIONS = json.load(file)

class Recommendations:
    def __init__(self, names=[], procedures={}, surgeries={}, labs={}, lifestyle_changes={}):
        self.names = names
        self.procedures = procedures
        self.surgeries = surgeries
        self.labs = labs
        self.lifestyle_changes = lifestyle_changes

    def set_values(self, names, data):
        for name in names:
            self.names.append(name)
            self.procedures[name] = DISEASE_RECOMMENDATIONS[name]["Procedures"]
            self.surgeries[name] = DISEASE_RECOMMENDATIONS[name]["Surgeries"]
            self.labs[name] = DISEASE_RECOMMENDATIONS[name]["Lab"]
            self.lifestyle_changes[name] = DISEASE_RECOMMENDATIONS[name]["Lifestyle changes"]
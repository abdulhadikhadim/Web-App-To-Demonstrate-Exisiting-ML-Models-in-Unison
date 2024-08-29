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
            self.procedures[name] = data[name]["Procedures"]
            self.surgeries[name] = data[name]["Surgeries"]
            self.labs[name] = data[name]["Lab"]
            self.lifestyle_changes[name] = data[name]["Lifestyle changes"]
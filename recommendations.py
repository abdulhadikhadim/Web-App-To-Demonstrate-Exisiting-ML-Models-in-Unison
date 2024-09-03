# import json
# with open("static/recommendations.json", "r") as file:
#     DISEASE_RECOMMENDATIONS = json.load(file)

# class Recommendations:
#     def __init__(self, names=[], procedures={}, surgeries={}, labs={}, lifestyle_changes={}):
#         self.names = names
#         self.procedures = procedures
#         self.surgeries = surgeries
#         self.labs = labs
#         self.lifestyle_changes = lifestyle_changes

#     def set_values(self, names, data):
#         for name in names:
#             if name not in self.names:
#                 self.names.append(name)
#                 self.procedures[name] = DISEASE_RECOMMENDATIONS[name]["Procedures"]
#                 self.surgeries[name] = DISEASE_RECOMMENDATIONS[name]["Surgeries"]
#                 self.labs[name] = DISEASE_RECOMMENDATIONS[name]["Labs"]
#                 self.lifestyle_changes[name] = DISEASE_RECOMMENDATIONS[name]["Lifestyle changes"]
#         # return self.names, self.procedures, self.surgeries, self.labs, self.lifestyle_changes


from dataclasses import dataclass, field
from typing import List, Dict, Any

# Assuming DISEASE_RECOMMENDATIONS is already loaded
import json
with open("static/recommendations.json", "r") as file:
    DISEASE_RECOMMENDATIONS = json.load(file)

@dataclass
class Recommendations:
    names: List[str] = field(default_factory=list)
    procedures: Dict[str, Any] = field(default_factory=dict)
    surgeries: Dict[str, Any] = field(default_factory=dict)
    labs: Dict[str, Any] = field(default_factory=dict)
    lifestyle_changes: Dict[str, Any] = field(default_factory=dict)

    def set_values(self, names: List[str], data: Dict[str, Any]) -> None:
        for name in names:
            if name not in self.names:
                self.names.append(name)
                self.procedures[name] = DISEASE_RECOMMENDATIONS.get(name, {}).get("Procedures", [])
                self.surgeries[name] = DISEASE_RECOMMENDATIONS.get(name, {}).get("Surgeries", [])
                self.labs[name] = DISEASE_RECOMMENDATIONS.get(name, {}).get("Labs", [])
                self.lifestyle_changes[name] = DISEASE_RECOMMENDATIONS.get(name, {}).get("Lifestyle changes", [])
        # Optional: Return the updated values if needed
        # return self.names, self.procedures, self.surgeries, self.labs, self.lifestyle_changes

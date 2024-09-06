from dataclasses import dataclass, field
from typing import List, Dict, Any

# Assuming DISEASE_RECOMMENDATIONS is already loaded
import json
with open("static/recommendations.json", "r") as file:
    DISEASE_RECOMMENDATIONS = json.load(file)
    
with open("static\disease_name_mapping.json", "r") as file:
    DISEASE_MAPPINGS = json.load(file)


with open("static\disease_name_mapping.json", "r") as file:
    DISEASE_MAPPINGS = json.load(file)

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
    def filter_recommendations(self, chronic_pred, medlab_pred):
        names = []
        for name in chronic_pred.names:
            if name != "BPH":
                if chronic_pred.prob[name]>=0.5:
                    names.append(DISEASE_MAPPINGS[name])
        if "normal" in medlab_pred.names:
            names.append("Normal")
        else:
            for name in medlab_pred.names:
                if medlab_pred.prob[name]>=60:
                    names.append(DISEASE_MAPPINGS[name])
        return names   

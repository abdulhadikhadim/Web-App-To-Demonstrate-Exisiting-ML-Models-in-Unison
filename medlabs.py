from dataclasses import dataclass, field
from typing import List, Dict, Any
from DiseasePredictor import DiseasePredictor

@dataclass
class MedLabPredictor(DiseasePredictor):
    confirmed_diag: Dict[str, Any] = field(default_factory=dict)

    def select_top_four(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        sorted_responses = sorted(data.get("likely_diag", []), key=lambda x: x.get('probability', 0), reverse=True)
        return sorted_responses[:4]

    def set_values(self, data: Dict[str, Any]) -> None:
        diagnosis = self.select_top_four(data)
        for disease in diagnosis:
            name = disease["disease_name"]
            if name not in self.names:
                self.names.append(name)
                self.prob[name] = disease["probability"]
                self.imp_features[name] = dict(sorted(disease["feature_importances"].items(), key=lambda item: item[1], reverse=True))
        for disease in data["confirmed_diag"]:
                    self.confirmed_diag[disease["verbose_name"]] = disease


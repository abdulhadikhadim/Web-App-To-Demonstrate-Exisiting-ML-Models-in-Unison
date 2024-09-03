# from DiseasePredictor import DiseasePredictor

# class MedLabPredictor(DiseasePredictor):
#     def __init__(self,names=[], prob={}, feature_imp={}):
#         super().__init__(names, prob, feature_imp)
        
#     def top_four_selector(self, data):
#         sorted_responses = sorted(data["likely_diag"], key=lambda x: x.get('probability', ''), reverse=True)
#         sorted_responses = sorted_responses[0:4]
#         return sorted_responses
    
#     def set_values(self,data):
#         diagnosis = self.top_four_selector(data)
#         for disease in diagnosis:
#             name = disease["disease_name"]
#             if name not in self.names:
#                 self.names.append(disease["disease_name"])
#                 self.prob[name] = disease["probability"]
#                 self.imp_features[name] = disease["feature_importances"]


from dataclasses import dataclass, field
from typing import List, Dict, Any
from DiseasePredictor import DiseasePredictor

@dataclass
class MedLabPredictor(DiseasePredictor):
    # feature_imp: Dict[str, Any] = field(default_factory=dict)

    def top_four_selector(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        sorted_responses = sorted(data.get("likely_diag", []), key=lambda x: x.get('probability', 0), reverse=True)
        return sorted_responses[:4]

    def set_values(self, data: Dict[str, Any]) -> None:
        diagnosis = self.top_four_selector(data)
        for disease in diagnosis:
            name = disease["disease_name"]
            if name not in self.names:
                self.names.append(name)
                self.prob[name] = disease["probability"]
                self.imp_features[name] = disease["feature_importances"]

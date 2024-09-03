
# class DiseasePredictor():
#     def __init__(self, names = [], prob = {}, imp_features = {}):
#         self.names = names
#         self.prob = prob
#         self.imp_features = imp_features
    
    
    
from typing import Any
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class DiseasePredictor:
    names: List[str] = field(default_factory=list)
    prob: Dict[str, float] = field(default_factory=dict)
    imp_features: Dict[str, Any] = field(default_factory=dict)

# Ensure that `Any` is imported from `typing` if used


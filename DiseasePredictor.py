from typing import Any
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class DiseasePredictor:
    names: List[str] = field(default_factory=list)
    prob: Dict[str, float] = field(default_factory=dict)
    imp_features: Dict[str, Any] = field(default_factory=dict)




from typing import Any
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class DiseasePredictor:
    """
    A class to store and manage disease prediction information.
    
    Attributes:
        names (List[str]): A list of disease names.
        prob (Dict[str, float]): A dictionary mapping disease names to their predicted probabilities.
        imp_features (Dict[str, Any]): A dictionary containing the important features for each disease.
    """
    names: List[str] = field(default_factory=list)
    prob: Dict[str, float] = field(default_factory=dict)
    imp_features: Dict[str, Any] = field(default_factory=dict)

    def set_values(self, data: Dict[str, Any]) -> None:
        """
        Sets the attributes of the DiseasePredictor using the provided data.
        
        Args:
            data (Dict[str, Any]): A dictionary containing the disease names, probabilities, and important features.
                                   Keys should include 'names', 'prob', and 'imp_features'.
        """
        # Update the list of disease names from the input data
        self.names = data["names"]
        
        # Update the probabilities for each disease from the input data
        self.prob = data["prob"]
        
        # Update the important features for each disease from the input data
        self.imp_features = data["imp_features"]

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import plotly.graph_objects as go
from DiseasePredictor import DiseasePredictor

@dataclass
class ChronicPredictor(DiseasePredictor):
    feature_vector: Dict[str, Any] = field(default_factory=dict)
    risky_features: Dict[str, Any] = field(default_factory=dict)
    top_pred_rules: Dict[str, Any] = field(default_factory=dict)
    trajectory: Optional[Dict[str, Any]] = None

    def set_values(self, data: Dict[str, Any]) -> None:
        for diseases in data["Content"]["DiseasePredictions"]:
            if diseases["Disease"] not in self.names:
                self.names.append(diseases["Disease"])
                # print(diseases["ModelsProbabilities"])
                # keys = diseases['ModelsProbabilities'].keys()
                # keys = keys.strip('_months')
                
                if "12_months" in diseases["ModelsProbabilities"]:
                    self.prob[diseases["Disease"]] = diseases["ModelsProbabilities"]["12_months"]
                else:
                    self.prob[diseases["Disease"]] = diseases["ModelsProbabilities"]["4_months"]
                self.feature_vector[diseases["Disease"]] = diseases["FeatureVector"]
                self.risky_features[diseases["Disease"]] = diseases["RiskyFeatures"]
                self.imp_features[diseases["Disease"]] = diseases["AllImportantFeatures"]
                self.top_pred_rules[diseases["Disease"]] = diseases["TopPredictionRules"]
        self.trajectory = data["Content"]["DiseaseTrajectories"]

    def generate_sankey_plot(self) -> Optional[go.Figure]:
        data = self.trajectory
        if data is None or "Mapper" not in data:
            return None

        id_to_desc = {item["ICD10"]: item["Description"] for item in data["Mapper"]}
        labels = list(set(item["From"] for item in data["Data"]) | set(item["To"] for item in data["Data"]))
        label_map = {label: idx for idx, label in enumerate(labels)}
        sources = [label_map[item["From"]] for item in data["Data"]]
        targets = [label_map[item["To"]] for item in data["Data"]]
        values = [item["Weight"] for item in data["Data"]]
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=[id_to_desc[label] for label in labels]
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values
            )
        )])
        fig.update_layout(title_text="Sankey Diagram of Disease Data", font_size=15)
        return fig




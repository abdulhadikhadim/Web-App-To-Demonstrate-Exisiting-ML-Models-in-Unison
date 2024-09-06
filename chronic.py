from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import plotly.graph_objects as go
from DiseasePredictor import DiseasePredictor

@dataclass
class ChronicPredictor(DiseasePredictor):
    """
    ChronicPredictor class extends DiseasePredictor and is used to predict
    chronic diseases based on given patient data. It also handles generating
    Sankey diagrams to visualize disease progression.

    Attributes:
        feature_vector (Dict[str, Any]): Stores the feature vector for each predicted disease.
        risky_features (Dict[str, Any]): Stores risky features for each predicted disease.
        top_pred_rules (Dict[str, Any]): Stores top prediction rules for each predicted disease.
        trajectory (Optional[Dict[str, Any]]): Stores disease trajectories for visualization.

    Methods:
        set_values(data: Dict[str, Any]) -> None: Sets disease prediction values from the provided data.
        generate_sankey_plot() -> Optional[go.Figure]: Generates a Sankey diagram visualizing disease trajectories.
    """
    # Feature vector containing detailed information about the patient's condition per disease.
    feature_vector: Dict[str, Any] = field(default_factory=dict)
    # Risky features that may contribute to the disease risk.
    risky_features: Dict[str, Any] = field(default_factory=dict)
    # Top rules that contributed to the prediction of the disease.
    top_pred_rules: Dict[str, Any] = field(default_factory=dict)
    # Disease trajectory mapping the progression of diseases over time.
    trajectory: Optional[Dict[str, Any]] = None

    def set_values(self, data: Dict[str, Any]) -> None:
        """
        Extracts and sets values for disease names, probabilities, feature vectors, risky features,
        important features, and top prediction rules from the input data.

        Args:
            data (Dict[str, Any]): A dictionary containing disease predictions and related information.
        """
        # Iterate through each disease in the predictions
        for diseases in data["Content"]["DiseasePredictions"]:
            # Add the disease name to the names list if it's not already there
            if diseases["Disease"] not in self.names:
                self.names.append(diseases["Disease"])

                # If "12_months" probability exists, use it; otherwise, default to "4_months"
                if "12_months" in diseases["ModelsProbabilities"]:
                    self.prob[diseases["Disease"]] = diseases["ModelsProbabilities"]["12_months"]
                else:
                    self.prob[diseases["Disease"]] = diseases["ModelsProbabilities"]["4_months"]

                # Store feature vectors, risky features, important features, and prediction rules
                self.feature_vector[diseases["Disease"]] = diseases["FeatureVector"]
                self.risky_features[diseases["Disease"]] = diseases["RiskyFeatures"]
                self.imp_features[diseases["Disease"]] = diseases["AllImportantFeatures"]
                self.top_pred_rules[diseases["Disease"]] = diseases["TopPredictionRules"]
        
        # Store the disease trajectory for visualization
        self.trajectory = data["Content"]["DiseaseTrajectories"]

    def generate_sankey_plot(self) -> Optional[go.Figure]:
        """
        Generates a Sankey diagram based on the disease trajectories data. If the required data
        is missing, it returns None.

        Returns:
            Optional[go.Figure]: A Plotly Sankey diagram figure or None if no valid data is available.
        """
        # Check if trajectory data is available
        data = self.trajectory
        if data is None or "Mapper" not in data:
            return None  # Return None if no data is available for plotting

        # Create a mapping of ICD10 codes to their descriptions
        id_to_desc = {item["ICD10"]: item["Description"] for item in data["Mapper"]}

        # Extract all unique "From" and "To" labels for the plot
        labels = list(set(item["From"] for item in data["Data"]) | set(item["To"] for item in data["Data"]))

        # Create a label map to convert labels into indices for Sankey plotting
        label_map = {label: idx for idx, label in enumerate(labels)}

        # Create lists of source, target, and values for the Sankey diagram
        sources = [label_map[item["From"]] for item in data["Data"]]
        targets = [label_map[item["To"]] for item in data["Data"]]
        values = [item["Weight"] for item in data["Data"]]

        # Generate the Sankey diagram using Plotly
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=[id_to_desc[label] for label in labels]  # Map labels to their descriptions
            ),
            link=dict(
                source=sources,  # Source nodes
                target=targets,  # Target nodes
                value=values     # Weights of the links
            )
        )])

        # Update the layout of the figure
        fig.update_layout(title_text="Sankey Diagram of Disease Data", font_size=15)
        return fig  # Return the figure object



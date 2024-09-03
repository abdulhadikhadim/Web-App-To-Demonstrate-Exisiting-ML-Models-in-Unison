import plotly.graph_objects as go

class ChronicDiseasePred:
    def __init__(self, feature_vector={}, important_features={}, risky_features={}, names=[], macro_rules = {}, top_pred_rules = {}, prob = {}, trajectory={}):
        self.names = names
        self.prob = prob
        self.feature_vector = feature_vector
        self.important_features = important_features
        self.risky_features = risky_features
        self.macro_rules = macro_rules
        self.top_pred_rules = top_pred_rules
        self.trajectory = trajectory


    def set_values(self, data):
        for diseases in data["Content"]["DiseasePredictions"]:
            if diseases["Disease"] not in self.names:
                self.names.append(diseases["Disease"])
                self.prob[diseases["Disease"]] = diseases["ModelsProbabilities"]["12_months"]
                self.feature_vector[diseases["Disease"]] = diseases["FeatureVector"]
                self.risky_features[diseases["Disease"]] = diseases["RiskyFeatures"]
                self.important_features[diseases["Disease"]] = diseases["AllImportantFeatures"]
                self.top_pred_rules[diseases["Disease"]] = diseases["TopPredictionRules"]
        self.trajectory=data["Content"]["DiseaseTrajectories"]

    def sankey_plot_generator(self):
        
        data = self.trajectory
        if "Mapper" not in data:  # Check if Mapper data is available
            self.has_sankey_data = False  # Set the flag to False if Mapper is missing
            return None

        # Create a mapping from ICD10 codes to descriptions
        id_to_desc = {item["ICD10"]: item["Description"] for item in data["Mapper"]}
        # Extract unique labels
        labels = list(set(item["From"] for item in data["Data"]) | set(item["To"] for item in data["Data"]))
        label_map = {label: idx for idx, label in enumerate(labels)}
        # Define sources, targets, and values for the Sankey plot
        sources = [label_map[item["From"]] for item in data["Data"]]
        targets = [label_map[item["To"]] for item in data["Data"]]
        values = [item["Weight"] for item in data["Data"]]
        # Create the Sankey plot
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

        # Update layout
        fig.update_layout(title_text="Sankey Diagram of Disease Data", font_size=15)
        return fig
        # fig.write_image("sankey_diagram.png")





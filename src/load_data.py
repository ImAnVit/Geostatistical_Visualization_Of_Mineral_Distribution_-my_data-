import pandas as pd

def load_dataset(path="data/geostatistical_visualization_anomalies.csv"):
    """Load 3D geostatistical research data with spatial coordinates and anomaly values."""
    data = pd.read_csv(path)
    return data
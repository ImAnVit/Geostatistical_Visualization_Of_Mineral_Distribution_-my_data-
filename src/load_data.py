import pandas as pd

def load_dataset(path="data/mineral_data.csv"):
    data = pd.read_csv(path)
    return data
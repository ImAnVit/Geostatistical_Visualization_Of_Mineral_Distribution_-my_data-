import numpy as np

def apply_fault_effect(data, fault_x=50, influence=10, strength=1.5):
    """
    Increase mineral values near a vertical fault line.
    """
    distance_to_fault = np.abs(data["x"] - fault_x)

    # Exponential decay effect
    effect = strength * np.exp(-distance_to_fault / influence)

    data["Ni"] = data["Ni"] + effect

    return data
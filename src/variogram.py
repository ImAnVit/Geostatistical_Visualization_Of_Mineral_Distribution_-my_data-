import numpy as np
from scipy.spatial.distance import pdist

def compute_variogram(x, y, z, bins=10):
    coords = np.column_stack((x, y))
    distances = pdist(coords)
    diffs = pdist(z.reshape(-1, 1))
    semivariance = 0.5 * diffs**2

    bin_edges = np.linspace(0, np.max(distances), bins)
    bin_indices = np.digitize(distances, bin_edges)

    bin_means = []
    bin_centers = []

    for i in range(1, len(bin_edges)):
        mask = bin_indices == i
        if np.any(mask):
            bin_means.append(np.mean(semivariance[mask]))
            bin_centers.append((bin_edges[i] + bin_edges[i-1]) / 2)

    return np.array(bin_centers), np.array(bin_means)
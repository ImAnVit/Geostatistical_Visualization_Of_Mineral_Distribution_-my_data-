import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.spatial import cKDTree

ANOMALY_PATH = "data/geostatistical_visualization_anomalies.csv"
MINERAL_PATH = "data/mineral_data.csv"


def load_anomaly_data(path=ANOMALY_PATH):
    return pd.read_csv(path)


def load_mineral_data(path=MINERAL_PATH):
    return pd.read_csv(path)


def combine_by_nearest_anomaly(anomalies: pd.DataFrame, minerals: pd.DataFrame):
    """Associate each mineral sample with its nearest anomaly sample in XY space."""
    anomalies_xy = anomalies[["X", "Y"]].to_numpy()
    minerals_xy = minerals[["x", "y"]].to_numpy()
    tree = cKDTree(anomalies_xy)
    distances, indices = tree.query(minerals_xy, k=1)

    nearest_anomalies = anomalies.iloc[indices].reset_index(drop=True)
    merged = pd.concat([
        minerals.reset_index(drop=True),
        nearest_anomalies[["Combined_Anomaly"]].rename(columns={"Combined_Anomaly": "Nearest_Combined_Anomaly"})
    ], axis=1)
    merged["Distance_to_Nearest_Anomaly"] = distances
    return merged


def estimate_anomaly_by_idw(anomalies: pd.DataFrame, minerals: pd.DataFrame, k=4, power=2):
    """Estimate anomaly at mineral points using inverse-distance weighting (IDW)."""
    anomalies_xy = anomalies[["X", "Y"]].to_numpy()
    minerals_xy = minerals[["x", "y"]].to_numpy()
    tree = cKDTree(anomalies_xy)
    distances, indices = tree.query(minerals_xy, k=k)

    # Ensure arrays are 2D for consistent indexing
    distances = np.atleast_2d(distances)
    indices = np.atleast_2d(indices)

    anomaly_vals = anomalies["Combined_Anomaly"].to_numpy()
    weights = np.where(distances == 0, np.inf, 1.0 / np.power(distances, power))

    # If any mineral point exactly matches an anomaly point, use that anomaly value directly
    exact_match = np.isinf(weights)
    estimates = np.zeros(len(minerals_xy), dtype=float)
    for i in range(len(minerals_xy)):
        if exact_match[i].any():
            estimates[i] = anomaly_vals[indices[i][exact_match[i]]][0]
        else:
            w = weights[i]
            vals = anomaly_vals[indices[i]]
            estimates[i] = np.dot(w, vals) / np.sum(w)

    idw_df = minerals.reset_index(drop=True).copy()
    idw_df["Estimated_Combined_Anomaly"] = estimates
    idw_df["IDW_k"] = k
    idw_df["IDW_power"] = power
    return idw_df


def combine_anomaly_estimates(anomalies: pd.DataFrame, minerals: pd.DataFrame):
    nearest = combine_by_nearest_anomaly(anomalies, minerals)
    idw = estimate_anomaly_by_idw(anomalies, minerals, k=4, power=2)
    return nearest.merge(idw[["id", "Estimated_Combined_Anomaly"]], on="id")


def summarize_relationship(merged: pd.DataFrame):
    if merged.empty:
        return "No merged records to analyze."

    summary_lines = [f"Merged records: {len(merged)}"]

    for label in ["Nearest_Combined_Anomaly", "Estimated_Combined_Anomaly"]:
        corr = merged["Ni"].corr(merged[label])
        slope, intercept = np.polyfit(merged[label], merged["Ni"], 1)
        merged["Anomaly_Quartile"] = pd.qcut(merged[label], 4, duplicates="drop")
        mean_by_quartile = merged.groupby("Anomaly_Quartile", observed=True)["Ni"].mean()

        summary_lines.append(f"\nUsing {label}:")
        summary_lines.append(f"  Correlation: {corr:.3f}")
        summary_lines.append(f"  Linear fit: Ni = {slope:.4f} * Anomaly + {intercept:.3f}")
        summary_lines.append(f"  Mean Ni by anomaly quartile:")
        summary_lines.append(mean_by_quartile.to_string())

    return "\n".join(summary_lines)


def plot_ni_vs_anomaly_comparison(merged: pd.DataFrame, output_path: str = "plots/ni_vs_anomaly_comparison.png"):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    for ax, label, title, color in [
        (axes[0], "Nearest_Combined_Anomaly", "Ni vs Nearest Combined Anomaly", "tab:blue"),
        (axes[1], "Estimated_Combined_Anomaly", "Ni vs Estimated Combined Anomaly", "tab:green"),
    ]:
        x = merged[label].to_numpy()
        y = merged["Ni"].to_numpy()
        slope, intercept = np.polyfit(x, y, 1)
        x_sorted = np.sort(x)
        y_line = slope * x_sorted + intercept

        ax.scatter(x, y, c=color, edgecolor="k", alpha=0.75)
        ax.plot(x_sorted, y_line, color="red", linestyle="--", label=f"Fit: Ni = {slope:.3f} * Anomaly + {intercept:.2f}")
        ax.set_xlabel(label.replace("_", " "))
        ax.set_title(title)
        ax.legend()
        ax.grid(alpha=0.3)

    axes[0].set_ylabel("Ni")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
    return output_path


def main():
    anomalies = load_anomaly_data()
    minerals = load_mineral_data()
    merged = combine_anomaly_estimates(anomalies, minerals)
    print(summarize_relationship(merged))

    output_path = "data/merged_mineral_anomaly_estimated.csv"
    merged.to_csv(output_path, index=False)
    print(f"Saved merged dataset to {output_path}")

    plot_path = plot_ni_vs_anomaly_comparison(merged)
    print(f"Saved comparison scatter plot to {plot_path}")


if __name__ == "__main__":
    main()

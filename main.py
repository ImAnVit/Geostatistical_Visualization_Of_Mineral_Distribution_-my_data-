from src.load_data import load_dataset
from src.visualization import plot_points, plot_points_3d, plot_surface_3d
from src.variogram import compute_variogram
from src.kriging_model import run_kriging, plot_kriging, plot_variance, apply_anisotropy, run_kriging_3d
from src.geology import apply_fault_effect

import matplotlib.pyplot as plt

def plot_coordinate_comparison(x, y, x_aniso, y_aniso, z):
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    scatter_orig = axs[0].scatter(x, y, c=z, edgecolor='k')
    axs[0].set_title("Original Coordinate Space")
    axs[0].set_xlabel("X")
    axs[0].set_ylabel("Y")
    fig.colorbar(scatter_orig, ax=axs[0], label="Ni concentration")

    scatter_aniso = axs[1].scatter(x_aniso, y_aniso, c=z, edgecolor='k')
    axs[1].set_title("Anisotropic Coordinate Space")
    axs[1].set_xlabel("X' (rotated)")
    axs[1].set_ylabel("Y' (stretched)")
    fig.colorbar(scatter_aniso, ax=axs[1], label="Ni concentration")

    plt.tight_layout()
    plt.show()


def main():
    # Load 3D research data
    data = load_dataset()

    # Extract 3D spatial coordinates and anomaly values
    x = data["X"].values
    y = data["Y"].values
    z = data["Profile"].values  # Third spatial dimension
    anomaly = data["Combined_Anomaly"].values

    print(f"Loaded {len(data)} spatial samples with coordinates:")
    print(f"  X range: {x.min():.1f} - {x.max():.1f}")
    print(f"  Y range: {y.min():.1f} - {y.max():.1f}")
    print(f"  Profile (Z) range: {z.min():.1f} - {z.max():.1f}")
    print(f"  Anomaly range: {anomaly.min():.1f} - {anomaly.max():.1f}")
    print()

    # Plot 1: 3D scatter of sample points
    print("Displaying 3D spatial distribution of sample points...")
    plot_points_3d(x, y, z, anomaly, title="3D Geostatistical Sample Points")

    # Plot 2: 3D Kriging prediction
    print("Computing 3D kriging predictions...")
    grid_x, grid_y, grid_z, z_pred, z_var = run_kriging_3d(x, y, z, anomaly)
    print(f"  Grid created: {len(grid_x)} x {len(grid_y)} x {len(grid_z)} = {len(grid_x) * len(grid_y) * len(grid_z)} predictions")
    print()

    # Plot 3: 3D Kriging surface
    print("Displaying 3D kriging prediction surface...")
    plot_surface_3d(grid_x, grid_y, grid_z, z_pred)


if __name__ == "__main__":
    main()
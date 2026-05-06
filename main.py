from src.load_data import load_dataset
from src.visualization import plot_points
from src.variogram import compute_variogram
from src.kriging_model import run_kriging, plot_kriging, plot_variance, apply_anisotropy
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
    # Load data
    data = load_dataset()

    # Apply geological fault effect
    data = apply_fault_effect(data, fault_x=50)

    x = data["x"].values
    y = data["y"].values
    z = data["Ni"].values

    # Plot updated points
    plot_points(data, element="Ni")

    # Apply anisotropy
    x_aniso, y_aniso = apply_anisotropy(x, y, angle_deg=30, ratio=2)

    # Compare original and anisotropic coordinates
    plot_coordinate_comparison(x, y, x_aniso, y_aniso, z)

    # Variogram (anisotropic)
    bin_centers, bin_means = compute_variogram(x_aniso, y_aniso, z)

    plt.plot(bin_centers, bin_means, 'o-')
    plt.title("Anisotropic Variogram")
    plt.xlabel("Distance")
    plt.ylabel("Semivariance")
    plt.grid()
    plt.show()

    # Kriging (with anisotropy)
    grid_x, grid_y, z_pred, z_var = run_kriging(x_aniso, y_aniso, z)

    # Plot prediction in anisotropic coordinate space
    plot_kriging(grid_x, grid_y, z_pred, x_aniso, y_aniso, z)
    plot_variance(grid_x, grid_y, z_var)


if __name__ == "__main__":
    main()
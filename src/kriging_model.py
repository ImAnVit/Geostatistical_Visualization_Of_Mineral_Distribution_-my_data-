import numpy as np
import matplotlib.pyplot as plt
from pykrige.ok import OrdinaryKriging

def apply_anisotropy(x, y, angle_deg=30, ratio=2):
    """
    Rotate and stretch coordinates to simulate anisotropy.
    """
    theta = np.radians(angle_deg)

    x_rot = x * np.cos(theta) + y * np.sin(theta)
    y_rot = -x * np.sin(theta) + y * np.cos(theta)

    # Stretch in one direction
    y_rot = y_rot * ratio

    return x_rot, y_rot

def run_kriging(x, y, z):
    grid_x = np.linspace(min(x), max(x), 100)
    grid_y = np.linspace(min(y), max(y), 100)

    OK = OrdinaryKriging(
        x, y, z,
        variogram_model='spherical',
        verbose=False,
        enable_plotting=False
    )

    z_pred, z_var = OK.execute('grid', grid_x, grid_y)

    return grid_x, grid_y, z_pred, z_var


def plot_kriging(grid_x, grid_y, z_pred, x, y, z, title="Kriging Prediction Map"):
    plt.imshow(
        z_pred,
        origin='lower',
        extent=(grid_x.min(), grid_x.max(), grid_y.min(), grid_y.max())
    )
    plt.scatter(x, y, c=z, edgecolor='k')
    plt.colorbar(label="Predicted Value")
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()


def plot_variance(grid_x, grid_y, z_var):
    plt.imshow(
        z_var,
        origin='lower',
        extent=(grid_x.min(), grid_x.max(), grid_y.min(), grid_y.max())
    )
    plt.colorbar(label="Variance")
    plt.title("Kriging Uncertainty Map")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()
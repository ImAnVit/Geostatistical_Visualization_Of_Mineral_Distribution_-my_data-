import numpy as np
import matplotlib.pyplot as plt
from pykrige.ok import OrdinaryKriging
from mpl_toolkits.mplot3d import Axes3D

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

def run_kriging_3d(x, y, z, values, grid_density=15):
    """Execute 2D ordinary kriging for each profile level to build 3D predictions."""
    grid_x = np.linspace(x.min(), x.max(), grid_density)
    grid_y = np.linspace(y.min(), y.max(), grid_density)
    unique_z = np.unique(z)
    grid_z = unique_z
    
    z_pred_3d = []
    z_var_3d = []
    
    # Krige each profile level separately
    for z_level in grid_z:
        mask = z == z_level
        if np.sum(mask) < 3:  # Need at least 3 points for kriging
            continue
            
        x_slice = x[mask]
        y_slice = y[mask]
        v_slice = values[mask]
        
        # Perform 2D kriging for this profile level
        OK = OrdinaryKriging(
            x_slice, y_slice, v_slice,
            variogram_model='spherical',
            verbose=False,
            enable_plotting=False
        )
        
        z_pred, z_var = OK.execute('grid', grid_x, grid_y)
        z_pred_3d.append(z_pred)
        z_var_3d.append(z_var)
    
    z_pred_3d = np.array(z_pred_3d)
    z_var_3d = np.array(z_var_3d)
    
    return grid_x, grid_y, grid_z, z_pred_3d, z_var_3d

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
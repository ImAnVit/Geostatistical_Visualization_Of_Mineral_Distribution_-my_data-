import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot_points(data, element="Ni"):
    plt.scatter(data["x"], data["y"], c=data[element], edgecolor='k')
    plt.colorbar(label=f"{element} concentration")
    plt.title(f"{element} Distribution (Sample Points)")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

def plot_points_3d(x, y, z, values, title="3D Spatial Distribution"):
    """Plot 3D scatter of spatial points with anomaly values as color."""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    scatter = ax.scatter(x, y, z, c=values, cmap='viridis', s=50, edgecolors='k')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Profile (Z)')
    ax.set_title(title)
    
    cbar = plt.colorbar(scatter, ax=ax, pad=0.1, label='Combined Anomaly')
    plt.tight_layout()
    plt.show()

def plot_surface_3d(grid_x, grid_y, grid_z, z_pred):
    """Plot 3D kriging prediction slices for each profile level."""
    fig = plt.figure(figsize=(12, 5))
    
    # Plot kriging results for each profile level as separate subplots
    for idx, z_level in enumerate(grid_z):
        if idx >= len(z_pred):
            break
            
        ax = fig.add_subplot(1, len(grid_z), idx + 1, projection='3d')
        
        # Create 2D meshgrid for this level
        XX, YY = np.meshgrid(grid_x, grid_y, indexing='ij')
        ZZ = np.full_like(XX, z_level)
        
        # Plot surface
        surf = ax.plot_surface(XX, YY, z_pred[idx], cmap='plasma', alpha=0.8)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Anomaly')
        ax.set_title(f'Profile {int(z_level)}')
        fig.colorbar(surf, ax=ax, shrink=0.5, label='Predicted Anomaly')
    
    plt.tight_layout()
    plt.show()
# Geostatistical 3D Visualization of Geophysical Anomalies

## Overview

This project demonstrates the application of geostatistics to model the **3D spatial distribution** of geophysical anomalies from research surveys in the Azov region. The workflow includes:

- **3D Data Integration**: Loading and processing real geophysical survey data with spatial (X, Y) and depth (Profile) coordinates
- **3D Kriging Analysis**: Performing 2D kriging per profile level to build 3D interpolation volumes
- **Variogram Modeling**: Understanding spatial dependence of anomaly distributions
- **Advanced Visualization**: Interactive 3D point clouds and kriging prediction surfaces
- **Anisotropy & Fault Modeling**: Incorporating geological structures to reflect real field conditions

The dataset is based on real geochemical anomaly data from the Azov region, including multi-component anomaly measurements (K1, K2, K3) and combined anomaly values across multiple survey profiles.

## Concepts Covered

This project focuses on several key concepts:

- **Geostatistics**: The study of spatially correlated data and modeling techniques like Kriging
- **3D Spatial Analysis**: Extending traditional 2D kriging to volumetric analysis across depth profiles
- **Fault-Controlled Mineralization**: Incorporating faults as structural factors influencing mineral concentration
- **Anisotropy**: The directional dependency of mineral distribution, often controlled by geological structures
- **Kriging Interpolation**: A method used to predict unknown values based on spatial correlation
- **Profile-Based Analysis**: Separating data by survey profile level for layer-by-layer kriging

## Objective

The main goals of the project are:

- **3D Data Visualization**: Render geophysical sample points in 3D space with anomaly values as color mapping
- **Volumetric Interpolation**: Predict anomaly values across a 3D grid using layer-stacked kriging
- **Uncertainty Quantification**: Assess prediction confidence through variance mapping
- **Anomaly Mapping**: Identify spatial patterns and anomaly distribution across profiles and coordinates

Key tasks include:

1. Load 3D geophysical survey data with coordinates (X, Y, Profile) and anomaly components
2. Extract and visualize anomaly spatial distribution in 3D
3. Perform kriging for each profile level independently
4. Generate 3D interpolation surfaces showing predicted anomaly values
5. Render interactive 3D visualizations of sample points and kriging results

## Methodology

### Step 1: Load and Prepare 3D Data

The 3D research data is loaded from a CSV file containing spatial coordinates and anomaly measurements. The dataset includes:
- **X, Y**: Horizontal spatial coordinates (in project units)
- **Profile**: Vertical/depth coordinate (survey profile number: 1, 2, 3, ...)
- **K1, K2, K3**: Three-component anomaly measurements
- **Combined_Anomaly**: Aggregate anomaly value for analysis

```python
# Load 3D Dataset
data = load_dataset("data/geostatistical_visualization_anomalies.csv")
x = data['X'].values
y = data['Y'].values
z = data['Profile'].values  # Third spatial dimension
anomaly = data['Combined_Anomaly'].values
```

### Step 2: 3D Point Cloud Visualization

Raw 3D sample points are visualized with anomaly values mapped to color intensity. This reveals the spatial structure and anomaly distribution patterns across the survey area.

```python
# Visualize 3D sample points
plot_points_3d(x, y, z, anomaly, title="3D Geostatistical Sample Points")
```

**What this shows:**
- Spatial clustering of high/low anomaly values
- Distribution across different profile levels
- Volumetric extent of the anomaly field

### Step 3: 3D Kriging - Per-Profile 2D Approach

Since full 3D kriging on scattered data requires advanced solvers, we implement **layer-based kriging**:

1. For each profile level (z), extract samples at that depth
2. Perform 2D ordinary kriging on the (X, Y) plane for that level
3. Generate predictions across a 2D grid at each profile
4. Stack all predicted grids to create a 3D volume

```python
# Execute 3D kriging
grid_x, grid_y, grid_z, z_pred, z_var = run_kriging_3d(x, y, z, anomaly)
```

**How it works:**
- Input: 23 sample points across 3 profile levels
- Process: 2D kriging per profile → 3D volume synthesis
- Output: 15×15×3 = 675 predictions in 3D space
- Variogram model: Spherical

### Step 4: 3D Kriging Surface Visualization

Kriging results are rendered as 3D surfaces, one per profile level. Each surface shows predicted anomaly values across the horizontal plane at that depth.

```python
# Visualize 3D kriging surfaces
plot_surface_3d(grid_x, grid_y, grid_z, z_pred)
```

**What this shows:**
- Smooth anomaly predictions interpolated between sample points
- Spatial trends and anomaly gradients
- Profile-by-profile comparison of predicted structure

### Step 5: Variogram Analysis (Optional)

Experimental variograms can be computed to quantify spatial dependence of anomalies:

```python
# Compute Variogram
bin_centers, bin_means = compute_variogram(x, y, anomaly)
```

This shows how anomaly correlation decreases with distance, informing the kriging variogram model selection.

### Step 6: Apply Anisotropy (Legacy Feature)

For traditional 2D workflows, anisotropy can be applied to simulate directional dependence:

```python
# Apply Anisotropy
x_aniso, y_aniso = apply_anisotropy(x, y, angle_deg=30, ratio=2)
```

This rotates and stretches coordinates to align with geological structures like fault lines.

## 3D Data & Spatial Concepts

### Multi-Profile Analysis

The dataset spans **3 survey profiles** (depth levels), each with spatial coordinates and anomaly measurements:
- **Profile 1**: 8 samples at Y=0
- **Profile 2**: 6 samples at Y=100
- **Profile 3**: 9 samples at Y=200

This layered structure enables true 3D volumetric analysis by kriging each layer and stacking results.

### Anomaly Components

The dataset includes three measured anomaly components (K1, K2, K3) which are combined into a **Combined_Anomaly** value for analysis:
- Range: 44–161 (anomaly units)
- Distribution: Non-uniform, concentrated at certain spatial locations

### 3D Grid & Predictions

The kriging grid spans the data domain:
- **X range**: 2–60 units
- **Y range**: 0–200 units  
- **Profile range**: 1–3 (discrete levels)
- **Grid resolution**: 15×15 per profile (225 points/level × 3 levels = 675 total)

## Faults and Anisotropy Explained

### 1. Fault Zones

In geological systems, fault zones represent structural controls that influence mineralization and anomaly distribution. The project includes a legacy fault modeling function that simulates higher anomaly concentrations near faults using exponential decay:

```python
data = apply_fault_effect(data, fault_x=50)
```

**Effect:** Mineral/anomaly concentrations increase as proximity to the fault decreases, modeling natural geological enrichment processes.

### 2. Anisotropy

Anisotropy reflects **directional variation** in geological properties. Mineralization and geophysical anomalies often follow directional patterns (fault trends, tectonic lineaments) rather than spreading uniformly in all directions.

Anisotropy is applied by rotating coordinates and stretching along a preferred direction:

```python
x_aniso, y_aniso = apply_anisotropy(x, y, angle_deg=30, ratio=2)
```

**Effect:** Kriging interpolation accounts for directional continuity, producing more realistic predictions aligned with geological structure.

### 3. 3D Kriging with Geological Context

By integrating fault effects and anisotropic properties into the kriging model, the 3D predictions become more geologically meaningful:
- Anomaly concentrations reflect structural controls
- Interpolation follows directional trends
- Results better represent actual subsurface conditions

## Project Structure

```
geostat-mineral-visualization_(my_data) - 3D/
│
├── data/                                          # Data folder
│   └── geostatistical_visualization_anomalies.csv # 3D research data (23 samples)
│
├── src/                                           # Source code folder
│   ├── load_data.py                              # 3D dataset loading
│   ├── visualization.py                          # 3D plotting functions
│   ├── variogram.py                              # Variogram computation
│   ├── kriging_model.py                          # 3D kriging implementation
│   └── geology.py                                # Fault & anisotropy modeling
│
├── main.py                                        # Main script (3D workflow)
├── requirements.txt                               # Python dependencies
└── README.md                                      # Project documentation
```

## Key Files

- **main.py**: Orchestrates the 3D analysis workflow
  - Loads data
  - Visualizes 3D sample points
  - Performs 3D kriging
  - Displays kriging surfaces

- **src/load_data.py**: Loads 3D CSV data with automatic coordinate extraction

- **src/visualization.py**: 
  - `plot_points_3d()`: 3D scatter of sample points
  - `plot_surface_3d()`: 3D surface meshes for kriging results

- **src/kriging_model.py**:
  - `run_kriging_3d()`: Per-profile 2D kriging stacking
  - Legacy `apply_anisotropy()` for coordinate transformation

- **src/geology.py**: Fault effect simulation (legacy feature)

## Technologies Used

- **Python**: Core programming language
- **NumPy**: Numerical computations and array operations
- **Pandas**: Data loading and manipulation
- **Matplotlib & mpl_toolkits.mplot3d**: 3D visualization and plotting
- **SciPy**: Spatial distance calculations for variogram
- **PyKrige (1.7.3)**: Ordinary kriging interpolation engine

## Installation & Setup

### 1. Clone or navigate to the repository:
```bash
cd geostat-mineral-visualization_(my_data)\ -\ 3D
```

### 2. Create and activate virtual environment (optional):
```bash
python -m venv myenv
myenv\Scripts\activate  # Windows
source myenv/bin/activate  # macOS/Linux
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Run the project:
```bash
python main.py
```

The script will generate interactive 3D plots showing:
1. Sample point cloud with anomaly color mapping
2. Kriging prediction surfaces for each profile level

## Output & Results

When you run `python main.py`, you'll see:

1. **Console Output:**
   - Data summary (sample count, coordinate ranges, anomaly statistics)
   - Grid generation info (15×15×3 = 675 predictions)

2. **Interactive Plots:**
   - **Plot 1**: 3D scatter of 23 research samples colored by Combined_Anomaly
   - **Plot 2**: 3D kriging surface slices (one per profile level)

3. **Visualization Features:**
   - Rotate, zoom, and pan 3D scenes
   - Color gradients show anomaly intensity
   - Axis labels and titles for interpretation

## Future Improvements

✅ **Completed:**
- 3D Kriging: Full volumetric interpolation via per-profile kriging stacking
- 3D Visualization: Interactive matplotlib-based 3D plotting
- Real Data Integration: Using actual geophysical survey data from research

🔄 **Potential Enhancements:**
- Interactive Visualizations: Upgrade to Plotly for web-based 3D exploration
- Volume Rendering: Add isosurface extraction for anomaly "bodies"
- Multi-Element Analysis: Simultaneous kriging of K1, K2, K3 components
- Uncertainty Quantification: 3D variance surfaces and confidence intervals
- Advanced Fault Modeling: Incorporate fault geometry directly into kriging weights
- Comparison Tools: Side-by-side view of different variogram models or anisotropy angles

## Author

**Vitaly Andriyko**  
Geology + Mathematics + Programming

## License

This project is open-source and available under the MIT License.

---

## Quick Start Command

```bash
python main.py
```

This executes the complete 3D geostatistical workflow: load data → visualize samples → compute kriging → render surfaces.

## Troubleshooting

**Issue:** ModuleNotFoundError: No module named 'pykrige'  
**Solution:** Run `pip install -r requirements.txt` to install all dependencies.

**Issue:** Plots don't appear  
**Solution:** Ensure your Python environment supports interactive matplotlib (use `%matplotlib` in Jupyter or run from terminal).

**Issue:** Memory or performance issues  
**Solution:** Reduce grid density in `run_kriging_3d()` (adjust `grid_density` parameter, default=15).

---

This comprehensive documentation explains the 3D geostatistical analysis workflow, from data preparation through kriging and visualization, and is ready for professional research or academic presentation!

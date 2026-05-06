# Geostatistical Mineral Visualization

A small geostatistics visualization project that loads mineral sample data and demonstrates:

- data loading from `data/mineral_data.csv`
- geological fault effect simulation
- anisotropy transformation of spatial coordinates
- experimental variogram calculation
- ordinary kriging prediction and uncertainty mapping
- matplotlib-based plot visualization

## Project Structure

- `main.py` - main execution script
- `src/load_data.py` - dataset loading helper
- `src/visualization.py` - plotting functions for sample points
- `src/variogram.py` - empirical variogram computation
- `src/kriging_model.py` - anisotropy transform, kriging execution, and plotting
- `src/geology.py` - geological fault effect simulation
- `data/mineral_data.csv` - input sample data
- `requirements.txt` - Python dependencies

## Requirements

This project is built for Python and depends on:

- `numpy`
- `pandas`
- `matplotlib`
- `scipy`
- `pykrige`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Activate your virtual environment if needed, then run:

```bash
python main.py
```

The script will:

1. load the mineral dataset
2. apply a simulated fault effect to nickel concentration
3. plot the sample points
4. apply anisotropy to the coordinates
5. compare original vs anisotropic coordinate spaces
6. compute and plot an empirical variogram
7. perform ordinary kriging and plot both predicted values and variance

## Notes

- The current implementation uses a fixed dataset path `data/mineral_data.csv`.
- Anisotropy is simulated by rotating and stretching coordinates.
- Fault effect is applied as an exponential decay boost to `Ni` values near a vertical fault line.

## License

This repository does not include a license file. Add one if you wish to make the code reusable by others.

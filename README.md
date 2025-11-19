# Magnet Simulation

Magnetic field simulation for a cylindrical Sm₂Co₁₇ (YXG-32H) permanent magnet.

## Overview

This project simulates and visualizes the magnetic field distribution around a cylindrical permanent magnet using analytical methods.

## Files

- `magnet_sim_2d.py` - 2D cross-section visualization (x-z plane)
- `magnet_sim_3d.py` - 3D interactive visualization with PyVista
- `INFO.md` - Detailed technical information and parameters

## Requirements

```bash
pip install magpylib numpy matplotlib pyvista
```

## Quick Start

### 2D Simulation
```bash
python magnet_sim_2d.py
```
Generates:
- 3D magnet model view
- x-z plane field distribution with streamlines
- Contour lines at 500, 1000, 2000 Gauss

### 3D Simulation
```bash
python magnet_sim_3d.py
```
Generates interactive 3D visualization with:
- x-z slice plane
- Field streamlines
- 2000 G isosurface contour

## Magnet Specifications

- **Material**: YXG-32H Sm₂Co₁₇
- **Dimensions**: Ø30 mm × 35 mm
- **Remanence**: 1.115 T
- **Magnetization**: z-axis

## Output

- Field strength in Gauss (G) or Tesla (T)
- Field lines showing magnetic flux direction
- Color-coded magnitude visualization

## License

MIT License

# Magnet Simulation - Technical Information

## Simulation Principle

### Magnetic Field Calculation Principles in Magpylib

Magpylib calculates the magnetic field of permanent magnets using **analytical** methods. Unlike numerical methods (such as FEM), it uses exact mathematical solutions.

#### 1. Equivalent Current Model

Permanent magnets are modeled as **equivalent surface currents**:
- Uniformly magnetized objects can be replaced by currents flowing on the surface
- Surface current density: $\mathbf{K} = \mathbf{M} \times \hat{\mathbf{n}}$ (M: magnetization, $\hat{\mathbf{n}}$: surface normal)

For cylindrical magnets:
- Circular surface current flowing on the lateral surface
- Same magnetic field distribution as a solenoid

#### 2. Biot-Savart Law

The fundamental principle starts from the Biot-Savart law:

$$d\mathbf{B} = \frac{\mu_0}{4\pi} \frac{I \, d\mathbf{l} \times \hat{\mathbf{r}}}{r^2}$$

Where:
- $\mu_0$: Permeability of free space
- $I$: Current
- $d\mathbf{l}$: Current element
- $r$: Distance to observation point

#### 3. Analytical Solution for Cylindrical Magnets

Magpylib uses exact analytical solutions with **Elliptic Integrals** for cylindrical magnets:

Axial magnetic field ($B_z$):

$$B_z = \frac{\mu_0 M}{4\pi} \left[ \text{integral expression with } K(k), E(k) \right]$$

Where $K(k)$ and $E(k)$ are complete elliptic integrals of the first and second kind, respectively.

Advantages of this method:
- Faster computation than FEM
- No mesh dependency
- Mathematically exact solution

#### 4. Superposition Principle

Complex geometries are calculated by superposition of basic magnets:

$$\mathbf{B}_{total} = \sum_i \mathbf{B}_i$$

### Magnetic Field Inside vs Outside the Magnet

**Outside ($r > R$)**:
- Magnetic dipole approximation (far field)
- Exact elliptic integral solution (near field)

**Inside ($r < R$)**:
- $\mathbf{B} = \mu_0(\mathbf{H} + \mathbf{M}) = \mu_0\mathbf{H} + B_r$
- Demagnetizing field considered

### Key Equations

- **Magnetization**: $M = \frac{B_r}{\mu_0}$ [A/m]
- **Magnetic permeability of vacuum**: $\mu_0 = 4\pi \times 10^{-7}$ [H/m]
- **Field units**: 1 T = 10,000 G (Gauss)
- **Surface current density**: $\mathbf{K} = \mathbf{M} \times \hat{\mathbf{n}}$ [A/m]

---

## Magnet Parameters (YXG-32H Sm₂Co₁₇)

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| **Material** | - | Sm₂Co₁₇ (Samarium Cobalt) | - |
| **Grade** | - | YXG-32H | - |
| **Remanence** | $B_r$ | 1.10 – 1.13 (avg: 1.115) | T |
| **Coercivity Force** | $H_{cb}$ | 812 – 860 (avg: 836) | kA/m |
| **Intrinsic Coercivity** | $H_{cj}$ | ≥ 1990 | kA/m |
| **Max Energy Product** | $(BH)_{max}$ | 230 – 255 (avg: 242.5) | kJ/m³ |
| **Max Working Temp** | - | 350 | °C |
| **Calculated Magnetization** | $M$ | $\sim 8.87 \times 10^5$ | A/m |

---

## Magnet Geometry

| Dimension | Value | Unit |
|-----------|-------|------|
| **Diameter (D)** | 30 | mm |
| **Height (H)** | 35 | mm |
| **Volume** | ~24,740 | mm³ |
| **Magnetization Direction** | +z axis | - |

---

## Visualization Details

### 2D Simulation (magnet_sim_2d.py)
- **Grid**: 300 × 300 points, -60 to +60 mm
- **Colormap**: coolwarm
- **Field lines**: Streamplot with density 1.5
- **Contours**: 500 G (cyan), 1000 G (lime), 2000 G (yellow)

### 3D Simulation (magnet_sim_3d.py)
- **Grid**: 61 × 61 × 61 points, -60 to +60 mm
- **Spacing**: 2 mm
- **Streamlines**: 15 radial seed points per pole
- **Slice plane**: x-z plane (y=0)
- **Isosurface**: 2000 G (0.2 T)

---

## Expected Field Values

| Position (z) | $|\mathbf{B}|$ (Gauss) | $|\mathbf{B}|$ (Tesla) |
|--------------|-------------|------------|
| Center (0 mm) | ~5,575 | ~0.558 |
| Surface (17.5 mm) | ~3,500 | ~0.350 |
| 1H away (35 mm) | ~1,200 | ~0.120 |
| 2H away (70 mm) | ~400 | ~0.040 |

*Note: Actual values may vary based on calculation resolution*

---

## Libraries Used

- **magpylib**: Analytical magnetic field calculations
- **numpy**: Numerical computations
- **matplotlib**: 2D plotting and 3D matplotlib backend
- **pyvista**: 3D visualization with interactive features

---

## References

1. Magpylib documentation: https://magpylib.readthedocs.io/
2. Sm₂Co₁₇ magnet datasheet: YXG-32H grade specifications

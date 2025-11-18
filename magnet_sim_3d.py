import magpylib as magpy
import pyvista as pv
import numpy as np

# ==========================
# YXG-32 Material Parameters
# ==========================
Br_min, Br_max = 1.10, 1.13  # [T]
Br = 0.5 * (Br_min + Br_max)  # 중간값 1.115 T

Hcb_min, Hcb_max = 812, 860  # [kA/m]
Hcb = 0.5 * (Hcb_min + Hcb_max) * 1e3  # A/m

Hcj = 1433e3  # ≥1433 kA/m -> A/m

BHmax_min, BHmax_max = 230, 255  # [kJ/m³]
BHmax = 0.5 * (BHmax_min + BHmax_max) * 1e3  # J/m³

mu0 = 4 * np.pi * 1e-7  # [H/m]
M = Br / mu0  # [A/m]

print("=" * 50)
print("YXG-32 Sm₂Co₁₇ Magnet Parameters")
print("=" * 50)
print(f"Remanence Br = {Br:.3f} T")
print(f"Coercivity Hcb = {Hcb/1e3:.1f} kA/m")
print(f"Intrinsic Coercivity Hcj ≥ {Hcj/1e3:.0f} kA/m")
print(f"(BH)max = {BHmax/1e3:.1f} kJ/m³")
print(f"Magnetization M = {M:.2e} A/m")
print("=" * 50)

# ==========================
# Cylinder Magnet Definition
# ==========================
D = 30  # 직경 [mm]
H = 35  # 높이 [mm]

magnet = magpy.magnet.Cylinder(
    polarization=(0, 0, Br),
    dimension=(D, H),
)

print(f"\nCylinder Magnet: D = {D} mm, H = {H} mm")

# ==========================
# 3D Grid for field calculation
# ==========================
grid = pv.ImageData(
    dimensions=(51, 51, 51),
    spacing=(2, 2, 2),  # 2mm spacing, directly in mm
    origin=(-50, -50, -50),  # -50mm to +50mm
)

# Compute B-field (grid is in mm, magpylib uses mm)
grid["B"] = magnet.getB(grid.points)  # result in T

# ==========================
# Streamlines from magnet poles
# ==========================
r_mag = D / 2  # 15 mm
h_mag = H / 2  # 17.5 mm

# Create seed points at top and bottom poles
n_seeds = 8  # angular divisions
angles = np.linspace(0, 2*np.pi, n_seeds, endpoint=False)
radii = [3, 8, 13]  # fewer radii for cleaner visualization

seed_points = []
for r in radii:
    for angle in angles:
        x = r * np.cos(angle)
        y = r * np.sin(angle)
        # Top pole
        seed_points.append([x, y, h_mag + 1])
        # Bottom pole
        seed_points.append([x, y, -h_mag - 1])

seed_points = np.array(seed_points)
seed = pv.PolyData(seed_points)

# Generate streamlines
strl = grid.streamlines_from_source(
    seed,
    vectors="B",
    max_step_length=1.0,
    max_time=200,
    integration_direction="both",
)

# ==========================
# Create Plotter
# ==========================
pl = pv.Plotter()

# Add magnet
magpy.show(magnet, canvas=pl, backend="pyvista")

# Add streamlines with thick tubes
legend_args = {
    "title": f"|B| (T)\nYXG-32\nBr={Br:.2f}T",
    "title_font_size": 14,
    "color": "black",
    "position_y": 0.25,
    "vertical": True,
}

pl.add_mesh(
    strl.tube(radius=0.3),  # thinner tube radius
    cmap="coolwarm",
    scalar_bar_args=legend_args,
)

# ==========================
# Add 3D arrows at grid points
# ==========================
arrow_grid = pv.ImageData(
    dimensions=(9, 9, 9),
    spacing=(10, 10, 10),  # 10mm spacing
    origin=(-40, -40, -40),
)

# Filter points outside magnet
pts = arrow_grid.points
r_pts = np.sqrt(pts[:, 0]**2 + pts[:, 1]**2)
z_pts = np.abs(pts[:, 2])
outside = ~((r_pts < r_mag) & (z_pts < h_mag))

pts_outside = pts[outside]
B_outside = magnet.getB(pts_outside)

# Create arrows
arrow_cloud = pv.PolyData(pts_outside)
arrow_cloud["B"] = B_outside
arrow_cloud["B_mag"] = np.linalg.norm(B_outside, axis=1)

arrows = arrow_cloud.glyph(
    orient="B",
    scale="B_mag",
    factor=50,  # large arrows
    geom=pv.Arrow(tip_length=0.3, tip_radius=0.15, shaft_radius=0.05),
)

pl.add_mesh(
    arrows,
    scalars="B_mag",
    cmap="coolwarm",
    show_scalar_bar=False,
)

# ==========================
# Camera and display
# ==========================
pl.camera.position = (120, 120, 80)
pl.camera.focal_point = (0, 0, 0)
pl.add_text(
    f"YXG-32 Cylinder Magnet\nD={D}mm, H={H}mm, Br={Br:.2f}T",
    position="upper_left",
    font_size=10,
    color="black",
)

pl.show()

import magpylib as magpy
import numpy as np
from matplotlib import pyplot as plt

"""
# YXG-32H Magnet Parameters

| 항목 | 값 |
|------|------|
| **Material** | Sm₂Co₁₇ (Sm2Co17 / Sm2(CoFeCuZr)17) |
| **Grade** | **YXG-32** |
| **Remanence Br** | **1.10 – 1.13 T** (11.0 – 11.3 kGs) |
| **Coercivity Force Hcb** | **812 – 860 kA/m** (10.2 – 10.8 kOe) |
| **Intrinsic Coercivity Hcj** | **≥1990 kA/m** (≥25 kOe) |
| **Maximum Energy Product (BH)max** | **230 – 255 kJ/m³** (29 – 32 MGOe) |
| **Max Working Temperature** | **350 °C** |
"""
# set font size
plt.rcParams.update({'font.size': 8})

# ==========================
# YXG-32 Material Parameters
# ==========================
# Remanence Br
Br_min, Br_max = 1.10, 1.13  # [T]
Br = 0.5 * (Br_min + Br_max)  # 중간값 1.115 T

# Coercivity Force Hcb
Hcb_min, Hcb_max = 812, 860  # [kA/m]
Hcb = 0.5 * (Hcb_min + Hcb_max) * 1e3  # 836 kA/m -> A/m

# Intrinsic Coercivity Hcj
Hcj = 1433e3  # ≥1433 kA/m -> A/m (minimum value)

# Maximum Energy Product (BH)max
BHmax_min, BHmax_max = 230, 255  # [kJ/m³]
BHmax = 0.5 * (BHmax_min + BHmax_max) * 1e3  # 242.5 kJ/m³ -> J/m³

# Physical constants
mu0 = 4 * np.pi * 1e-7  # [H/m]

# Magnetization
M = Br / mu0  # [A/m] ≈ 8.87e5 A/m

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

# create cylinder magnet
cylinder = magpy.magnet.Cylinder(
    polarization=(0, 0, Br),  # z-axis magnetization [T]
    dimension=(D, H),          # (diameter, height) in mm
)

print(f"\nCylinder Magnet: D = {D} mm, H = {H} mm")
print(f"Volume = {np.pi * (D/2)**2 * H:.1f} mm³")

# ==========================
# Position Grid
# ==========================
ts = np.linspace(-60, 60, 300)  # -60 to +60 mm (higher resolution)
grid_size = len(ts)

# x-z plane (y=0)
posis_xz = np.array([(x, 0, z) for z in ts for x in ts])
X_xz, Z_xz = np.meshgrid(ts, ts)

# ==========================
# Create Figure with 2 Subplots
# ==========================
fig = plt.figure(figsize=(18, 10))
ax3d = fig.add_subplot(1, 2, 1, projection='3d')
ax_xz = fig.add_subplot(1, 2, 2)
plt.subplots_adjust(wspace=0.3)  # Wider spacing between plots

# 3D display - custom smooth cylinder
from mpl_toolkits.mplot3d import art3d
from matplotlib import cm

# Create smooth cylinder surface
theta_cyl = np.linspace(0, 2*np.pi, 100)
z_cyl = np.linspace(-H/2, H/2, 60)
Theta_cyl, Z_cyl_mesh = np.meshgrid(theta_cyl, z_cyl)
X_cyl = (D/2) * np.cos(Theta_cyl)
Y_cyl = (D/2) * np.sin(Theta_cyl)

# Plot cylinder surface (gray, opaque)
ax3d.plot_surface(X_cyl, Y_cyl, Z_cyl_mesh, color='gray', alpha=1.0)

# Plot top and bottom caps
theta_cap = np.linspace(0, 2*np.pi, 100)
r_cap = np.linspace(0, D/2, 20)
Theta_cap, R_cap = np.meshgrid(theta_cap, r_cap)
X_cap = R_cap * np.cos(Theta_cap)
Y_cap = R_cap * np.sin(Theta_cap)

# Top cap
Z_top = np.ones_like(X_cap) * H/2
ax3d.plot_surface(X_cap, Y_cap, Z_top, color='gray', alpha=1.0)

# Bottom cap
Z_bot = np.ones_like(X_cap) * (-H/2)
ax3d.plot_surface(X_cap, Y_cap, Z_bot, color='gray', alpha=1.0)

# Add 3D blue arrow for magnetization direction (thinner)
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Create 3D arrow shaft - positioned above cylinder
arrow_length = H * 0.25  # Half of previous length
shaft_radius = 0.8
tip_length = arrow_length * 0.3
tip_radius = 1.5
arrow_base = H/2 + 2  # Start above the cylinder top

# Shaft cylinder
n_points = 20
theta_arr = np.linspace(0, 2*np.pi, n_points)
z_shaft = np.linspace(arrow_base, arrow_base + arrow_length - tip_length, 10)
Theta_shaft, Z_shaft = np.meshgrid(theta_arr, z_shaft)
X_shaft = shaft_radius * np.cos(Theta_shaft)
Y_shaft = shaft_radius * np.sin(Theta_shaft)
ax3d.plot_surface(X_shaft, Y_shaft, Z_shaft, color='blue', alpha=0.9)

# Arrow tip cone
z_tip = np.linspace(arrow_base + arrow_length - tip_length, arrow_base + arrow_length, 10)
for i in range(len(z_tip)-1):
    r1 = tip_radius * (1 - (z_tip[i] - (arrow_base + arrow_length - tip_length)) / tip_length)
    r2 = tip_radius * (1 - (z_tip[i+1] - (arrow_base + arrow_length - tip_length)) / tip_length)
    x1 = r1 * np.cos(theta_arr)
    y1 = r1 * np.sin(theta_arr)
    x2 = r2 * np.cos(theta_arr)
    y2 = r2 * np.sin(theta_arr)
    for j in range(len(theta_arr)-1):
        verts = [[x1[j], y1[j], z_tip[i]], [x1[j+1], y1[j+1], z_tip[i]],
                 [x2[j+1], y2[j+1], z_tip[i+1]], [x2[j], y2[j], z_tip[i+1]]]
        ax3d.add_collection3d(Poly3DCollection([verts], color='blue', alpha=0.9))

ax3d.set_xlabel('x [mm]')
ax3d.set_ylabel('y [mm]')
ax3d.set_zlabel('z [mm]')
ax3d.set_title(f'YXG-32 Cylinder Magnet\n(D={D}mm, H={H}mm, Br={Br:.2f}T)')
ax3d.set_box_aspect([1, 1, H/D])

# Add grid
ax3d.grid(True)

# Set initial view angle - Miller index (110) direction
ax3d.view_init(elev=0, azim=45)

# Set axis limits
ax3d.set_xlim([-30, 30])
ax3d.set_ylim([-30, 30])
ax3d.set_zlim([-30, 30])

# ==========================
# x-z plane field plot (y=0)
# ==========================
B_xz = cylinder.getB(posis_xz).reshape(grid_size, grid_size, 3)
B_magnitude_xz = np.linalg.norm(B_xz, axis=2)

# pcolor for amplitude (convert T to Gauss: 1 T = 10000 G)
B_magnitude_xz_G = B_magnitude_xz * 10000
pcm_xz = ax_xz.pcolor(X_xz, Z_xz, B_magnitude_xz_G, cmap='coolwarm', shading='auto')
cbar_xz = plt.colorbar(pcm_xz, ax=ax_xz, shrink=0.65)
cbar_xz.set_label('|B| [G]')

# streamplot for field lines
ax_xz.streamplot(X_xz, Z_xz, B_xz[:, :, 0], B_xz[:, :, 2], color='k', linewidth=0.5, density=1.5)

# Contour for 500, 1000, 2000 Gauss
contour_lines = ax_xz.contour(X_xz, Z_xz, B_magnitude_xz_G, levels=[500, 1000, 2000], colors=['cyan', 'lime', 'yellow'], linewidths=2)
ax_xz.clabel(contour_lines, fmt='%d G', fontsize=8)

# Draw magnet outline
rect_x = [-D/2, D/2, D/2, -D/2, -D/2]
rect_z = [-H/2, -H/2, H/2, H/2, -H/2]
ax_xz.plot(rect_x, rect_z, 'g-', linewidth=2, label='Magnet')

ax_xz.set_xlabel('x [mm]')
ax_xz.set_ylabel('z [mm]')
ax_xz.set_title(f'B-field (x-z plane, y=0)\nYXG-32: Br={Br:.2f}T')
ax_xz.set_aspect('equal')
ax_xz.legend(loc='upper right')

plt.tight_layout()
plt.show()

# ==========================
# Print Field Values at Key Points
# ==========================
print("\n" + "=" * 50)
print("Magnetic Field at Key Points")
print("=" * 50)

# On-axis points
z_points = [0, H/2, H, 2*H]  # center, surface, 1H away, 2H away
for z_pt in z_points:
    B_pt = cylinder.getB([0, 0, z_pt])
    B_G = B_pt[2] * 10000  # T to Gauss
    print(f"z = {z_pt:5.1f} mm: Bz = {B_G:8.2f} G ({B_pt[2]:.4f} T)")

print("=" * 50)
"""
Blender script: Magnet Ring - Simple Cylinders
Run in Blender: Scripting tab → plakken → Run Script
"""

import bpy
import math
import numpy as np
from mathutils import Matrix

# ── INPUTS ──
N    = 12
p    = 3
configuratie = 0   # 0 = Halbach, 1 = Parallel

rmag = 15e-3 / 2
hmag = 8e-3  / 2   # zmag = hmag
r    = N * rmag / math.pi

SCALE = 1000  # metres naar milimeters

# code voor rotatie langs cirkel

def local_frame(theta, conf, p):
    r_hat   = np.array([ math.cos(theta),  math.sin(theta), 0.0])
    phi_hat = np.array([-math.sin(theta),  math.cos(theta), 0.0])
    z_hat   = np.array([0.0, 0.0, 1.0])

    if conf == "Halbach":
        alpha  = p * theta
        nu_hat = math.sin(alpha) * phi_hat + math.cos(alpha) * z_hat
        t_hat  = r_hat
        s_hat  = np.cross(nu_hat, t_hat)
        s_hat /= np.linalg.norm(s_hat)
    else:  # Parallel
        nu_hat = -z_hat
        s_hat  = r_hat
        t_hat  = phi_hat

    return nu_hat, s_hat, t_hat

conf = "Halbach" if configuratie == 0 else "Parallel"
zmag = hmag

# bouw de cilinders
for i in range(N):
    theta  = 2 * math.pi * i / N
    centre = np.array([r * math.cos(theta), r * math.sin(theta), 0.0])
    nu_hat, s_hat, t_hat = local_frame(theta, conf, p)

    bpy.ops.mesh.primitive_cylinder_add(
        radius=rmag * SCALE,
        depth=2 * zmag * SCALE,
        vertices=32,
        location=(0, 0, 0),
    )
    cyl = bpy.context.active_object
    cyl.name = f"Magnet_{i:02d}"

    s = SCALE
    cyl.matrix_world = Matrix([
        [t_hat[0],  s_hat[0],  nu_hat[0],  centre[0] * s],
        [t_hat[1],  s_hat[1],  nu_hat[1],  centre[1] * s],
        [t_hat[2],  s_hat[2],  nu_hat[2],  centre[2] * s],
        [0.0,       0.0,       0.0,        1.0           ],
    ])

print(f"Done: {N} cylinders, conf={conf}, r={r*1000:.1f}mm, rmag={rmag*1000:.1f}mm")
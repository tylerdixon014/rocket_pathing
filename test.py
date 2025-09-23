import numpy as np
import quaternion as qtn 
from silly_billy_math import Spline

def _safe_normalize(v, eps=1e-12):
    n = np.linalg.norm(v)
    if n < eps:
        raise ValueError("Vector too small to normalize")
    return v / n

def _axis_angle_quat(axis, angle_rad):
    axis = _safe_normalize(axis)
    half = angle_rad * 0.5
    return qtn.quaternion(np.cos(half), *(axis * np.sin(half)))

def look_quat_from_tangent(t_vec, world_up=np.array([0.0, 0.0, 1.0])):
    """
    Create a 'look' orientation:
    - forward (local +X) aligns to t_vec
    - tries to keep local +Z close to world_up
    Returns a quaternion (w, x, y, z).
    """
    f = _safe_normalize(np.asarray(t_vec, dtype=float))  # forward
    up = np.asarray(world_up, dtype=float)

    # If forward is too close to up, pick an alternate up to avoid degeneracy
    if np.linalg.norm(np.cross(f, up)) < 1e-8:
        up = np.array([0.0, 1.0, 0.0])

    r = _safe_normalize(np.cross(up, f))   # right
    u = np.cross(f, r)                      # corrected up (orthonormal)

    # Rotation matrix with columns = [forward, right, up]
    R = np.column_stack([f, r, u])

    # Convert to quaternion
    # numpy-quaternion exposes from_rotation_matrix via the module
    q_look = qtn.from_rotation_matrix(R)
    return q_look

def quaternion_from_tangent_and_roll(t_vec, roll_rad, world_up=np.array([0.0, 0.0, 1.0])):
    """
    Return quaternion rotating from 'straight upright' (forward=+X, up=+Z)
    to:
      - forward aligned with t_vec
      - rolled by roll_rad around that forward axis
    """
    q_look = look_quat_from_tangent(t_vec, world_up=world_up)
    f = _safe_normalize(np.asarray(t_vec, dtype=float))
    q_roll = _axis_angle_quat(f, roll_rad)
    q_final = q_roll * q_look
    return q_final


filepath = "sample.csv"
sensor = [1,1,1]

spline = Spline(filepath)

t = 1 
tangent = spline.evaluate(t)
angle = spline.total_rotation(t)
q = quaternion_from_tangent_and_roll(tangent, angle)

print(q)

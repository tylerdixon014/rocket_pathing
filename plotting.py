import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math_stuff import math_functions


file_path = "rocket simulation sample points.csv"

def main():
    

    # Parameter t
    t = np.linspace(0, 1,20)

    x = 0
    y = t
    z = 0

    # Set up figure and 3D axis
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")

    # Plot parametric line
    ax.plot3D(x, y, z, color="blue", linewidth=2)

    # Labels and title
    ax.set_title("3D Parametric Line: Helix")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    plt.show()

def read_csv(file_path):
    df = pd.read_csv(file_path)

    pos_points = df["position points"].apply(lambda s: list(map(float, s.split(",")))).to_numpy()
    pos_points = np.vstack(pos_points)

    con_points = df["control points"].apply(lambda s: list(map(float, s.split(",")))).to_numpy()
    con_points = np.vstack(con_points)

    return pos_points, pos_points



main()

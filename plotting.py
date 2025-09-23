import numpy as np
import matplotlib.pyplot as plt
from silly_billy_math import Spline

filepath = "sample.csv"
sensor = [0.1,0.1,0.25]

spline = Spline(filepath)

def main():
    # Parameter t
    t = np.linspace(min(spline.time_list), max(spline.time_list) - 0.1,100)

    x = []
    y = []
    z = []
    sx = []
    sy = []
    sz = []
    for i in t:
        com = spline.evaluate(i)
        x.append(com[0])
        y.append(com[1])
        z.append(com[2])
        sensor_pos = spline.sensor(sensor,i)
        sx.append(sensor_pos[0])
        sy.append(sensor_pos[1])
        sz.append(sensor_pos[2])


    # Set up figure and 3D axis
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")

    # Plot parametric line
    ax.plot3D(x, y, z, color="blue", linewidth=2)
    ax.plot3D(sx, sy, sz, color="red", linewidth=2)

    # Labels and title
    ax.set_title("Bezier Spline")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    plt.show()

main()
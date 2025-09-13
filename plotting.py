import numpy as np
import matplotlib.pyplot as plt
from math_stuff import parametric_plot

def main():
    # Parameter t
    t = np.linspace(0, 1,20)


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

print(parametric_plot.test)
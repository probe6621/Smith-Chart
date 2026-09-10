"""
Example script to visualize the Toroidal Smith Chart using Matplotlib in Python/VS Code.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from core.transformer import ToroidalSmithTransformer
from core.plenum_density import PlenumDensityField


def plot_toroidal_smith_chart():
    transformer = ToroidalSmithTransformer(base_impedance=50.0)
    plenum = PlenumDensityField()

    # Generate impedance grid (Resistance R and Reactance X)
    r_vals = np.logspace(-1, 2, 30)
    x_vals = np.linspace(-100, 100, 30)
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#05050a')
    fig.patch.set_facecolor('#05050a')

    t = 0.5
    rho_field = np.ones((10, 10)) * 1.2

    # Plot constant resistance and reactance trajectories mapped to torus
    for r in r_vals[::3]:
        coords_list = []
        for x in x_vals:
            Z = complex(r, x)
            pt = transformer.map_to_toroidal(Z, rho_field, t)
            coords_list.append(pt)
        coords_list = np.array(coords_list)
        ax.plot(coords_list[:, 0], coords_list[:, 1], coords_list[:, 2], color='#00ffcc', alpha=0.6, linewidth=1)

    for x in x_vals[::3]:
        coords_list = []
        for r in r_vals:
            Z = complex(r, x)
            pt = transformer.map_to_toroidal(Z, rho_field, t)
            coords_list.append(pt)
        coords_list = np.array(coords_list)
        ax.plot(coords_list[:, 0], coords_list[:, 1], coords_list[:, 2], color='#00aaff', alpha=0.6, linewidth=1)

    ax.set_title("3D Toroidal Smith Chart Surface", color='#00ffcc', fontsize=14)
    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig("toroidal_smith_chart.png", dpi=150, facecolor=fig.get_facecolor())
    print("Saved toroidal_smith_chart.png")
    plt.show()


if __name__ == "__main__":
    plot_toroidal_smith_chart()

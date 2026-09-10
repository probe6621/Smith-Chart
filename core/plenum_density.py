import numpy as np


class PlenumDensityField:
    """
    Manages spatial and temporal vacuum-density distributions rho(x, t).
    """
    def __init__(self, grid_shape=(50, 50), default_density=1.0):
        self.grid_shape = grid_shape
        self.default_density = default_density

    def compute_density(self, x_grid, t, frequency=1.0, scale=0.15):
        """
        Computes space-time density field rho(x, t) = rho_0 * (1 + scale * sin(freq * x + t)).
        """
        return self.default_density * (1.0 + scale * np.sin(frequency * x_grid + t))

    def density_gradient(self, rho_field):
        """
        Calculates spatial gradient of the density field.
        """
        return np.gradient(rho_field)

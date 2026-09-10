import numpy as np


class BoundaryEnergyVectors:
    """
    Calculates boundary flux and coupling energy exchange vectors across resistive loss circles in toroidal space.
    """
    def __init__(self, transformer=None):
        self.transformer = transformer

    def compute_flux(self, gamma, rho_val):
        """
        Computes boundary energy flux vector given reflection coefficient gamma and local plenum density.
        """
        power_reflection = np.abs(gamma) ** 2
        power_transmission = 1.0 - power_reflection
        flux_magnitude = power_transmission * rho_val
        phase = np.angle(gamma)

        # 2D flux components in complex reflection plane
        fx = flux_magnitude * np.cos(phase)
        fy = flux_magnitude * np.sin(phase)
        return np.array([fx, fy])

    def coupling_vector_3d(self, toroidal_coords, flux_vector):
        """
        Maps 2D flux vector to 3D toroidal surface tangent direction.
        """
        norm_coords = toroidal_coords / (np.linalg.norm(toroidal_coords) + 1e-12)
        tangent_x = -norm_coords[1]
        tangent_y = norm_coords[0]
        tangent_z = norm_coords[2]
        tangent = np.array([tangent_x, tangent_y, tangent_z])
        return tangent * np.linalg.norm(flux_vector)

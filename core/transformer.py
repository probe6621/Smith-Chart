import numpy as np


class ToroidalSmithTransformer:
    def __init__(self, base_impedance=50.0):
        self.Z_0 = base_impedance

    def reflection_coefficient(self, Z):
        """Calculates standard complex reflection coefficient Gamma."""
        return (Z - self.Z_0) / (Z + self.Z_0)

    def dynamic_plenum_density_z0(self, rho_field, t):
        """Adjusts baseline impedance dynamically based on local vacuum-gradient density rho(x,t)."""
        # Epsilon Framework scaling relation for baseline impedance shift
        return self.Z_0 * (1.0 + np.mean(rho_field) * np.sin(t))

    def map_to_toroidal(self, Z, rho_field, t, R_major=2.0, r_minor=1.0):
        """
        Maps standard impedance and dynamic reflection coefficient 
        onto a 3D toroidal surface (poloidal theta, toroidal phi).
        """
        current_z0 = self.dynamic_plenum_density_z0(rho_field, t)
        gamma = (Z - current_z0) / (Z + current_z0)
        
        # Map magnitude to poloidal angle and phase to toroidal angle
        mag = np.abs(gamma)
        phase = np.angle(gamma)
        
        theta = np.pi * mag  # Bounded radial projection to poloidal angle
        phi = phase          # Phase maps directly to toroidal sweep
        
        # Parametric torus equations incorporating field modulation
        x = (R_major + r_minor * np.cos(theta)) * np.cos(phi)
        y = (R_major + r_minor * np.cos(theta)) * np.sin(phi)
        z = r_minor * np.sin(theta)
        
        return np.array([x, y, z])

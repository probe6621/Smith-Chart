import unittest
import numpy as np

from core.transformer import ToroidalSmithTransformer
from core.plenum_density import PlenumDensityField
from core.energy_vectors import BoundaryEnergyVectors


class TestToroidalSmithTransformer(unittest.TestCase):

    def setUp(self):
        self.transformer = ToroidalSmithTransformer(base_impedance=50.0)
        self.plenum = PlenumDensityField()
        self.energy = BoundaryEnergyVectors(self.transformer)

    def test_reflection_coefficient_matched(self):
        """Matched load (Z = Z0) should yield Gamma = 0."""
        gamma = self.transformer.reflection_coefficient(50.0)
        self.assertAlmostEqual(gamma, 0.0 + 0.0j)

    def test_reflection_coefficient_open(self):
        """Open circuit (Z -> infinity) should yield Gamma -> 1."""
        gamma = self.transformer.reflection_coefficient(1e9)
        self.assertAlmostEqual(np.abs(gamma), 1.0, places=4)

    def test_reflection_coefficient_short(self):
        """Short circuit (Z = 0) should yield Gamma = -1."""
        gamma = self.transformer.reflection_coefficient(0.0)
        self.assertAlmostEqual(gamma, -1.0 + 0.0j)

    def test_dynamic_plenum_density(self):
        """Check dynamic Z0 adjustment with non-zero density field."""
        rho_field = np.ones((10, 10)) * 1.5
        t = np.pi / 2  # sin(pi/2) = 1
        z0_dyn = self.transformer.dynamic_plenum_density_z0(rho_field, t)
        # Z0 * (1 + 1.5 * 1.0) = 50 * 2.5 = 125.0
        self.assertAlmostEqual(z0_dyn, 125.0)

    def test_map_to_toroidal_shape(self):
        """Toroidal mapping should return a 3-element coordinate array [x, y, z]."""
        Z = 75.0 + 25.0j
        rho_field = np.ones((5, 5))
        t = 0.5
        coords = self.transformer.map_to_toroidal(Z, rho_field, t)
        self.assertEqual(coords.shape, (3,))
        self.assertFalse(np.any(np.isnan(coords)))

    def test_plenum_density_field(self):
        """Test spatial-temporal density field calculation."""
        x_grid = np.linspace(0, 10, 20)
        field = self.plenum.compute_density(x_grid, t=0.0)
        self.assertEqual(field.shape, (20,))
        self.assertTrue(np.all(field >= 0.0))

    def test_boundary_energy_vectors(self):
        """Test boundary flux vector calculation."""
        gamma = 0.5 + 0.0j
        flux = self.energy.compute_flux(gamma, rho_val=1.0)
        # power_transmission = 1 - 0.25 = 0.75
        self.assertAlmostEqual(flux[0], 0.75)
        self.assertAlmostEqual(flux[1], 0.0)


    def test_standard_smith_anchor_points(self):
        """Verify baseline anchor points against standard RF values at baseline Z0 = 50 ohms."""
        transformer = ToroidalSmithTransformer(base_impedance=50.0)
        
        # 1. Matched load (Z = 50) -> Center of chart (Gamma = 0)
        gamma_matched = transformer.reflection_coefficient(50.0)
        self.assertAlmostEqual(np.abs(gamma_matched), 0.0)
        
        # 2. Short circuit (Z = 0) -> Extreme left (Gamma = -1)
        gamma_short = transformer.reflection_coefficient(0.0)
        self.assertAlmostEqual(gamma_short, -1.0 + 0.0j)
        
        # 3. Open circuit (Z -> infinity) -> Extreme right (Gamma = +1)
        gamma_open = transformer.reflection_coefficient(1e9)
        self.assertAlmostEqual(np.abs(gamma_open), 1.0, places=4)
        self.assertAlmostEqual(np.angle(gamma_open), 0.0, places=4)

        # 4. Pure reactance (Z = j50) -> Lies on unit circle perimeter (|Gamma| = 1)
        gamma_reactance = transformer.reflection_coefficient(50.0j)
        self.assertAlmostEqual(np.abs(gamma_reactance), 1.0)
        self.assertAlmostEqual(np.angle(gamma_reactance), np.pi / 2)


    def test_toroidal_mapping_bounds_across_varying_densities(self):
        """Verify that mapping coordinates remain mathematically bounded for various density inputs."""
        R_major = 2.0
        r_minor = 1.0
        max_possible_radius = R_major + r_minor + 1e-6

        # Test across range of impedances, times, and density fields
        densities = [0.1, 0.5, 1.0, 2.5, 10.0]
        impedances = [0.0, 50.0, 100.0 + 50.0j, 1e6]
        times = [0.0, np.pi/4, np.pi/2, np.pi, 2*np.pi]

        for rho_val in densities:
            rho_field = np.full((10, 10), rho_val)
            for z_val in impedances:
                for t in times:
                    coords = self.transformer.map_to_toroidal(
                        z_val, rho_field, t, R_major=R_major, r_minor=r_minor
                    )
                    dist = np.linalg.norm(coords)
                    self.assertLessEqual(
                        dist, 
                        max_possible_radius, 
                        f"Point distance {dist} exceeded maximum torus bound {max_possible_radius} for rho={rho_val}, Z={z_val}, t={t}"
                    )
                    self.assertFalse(np.any(np.isnan(coords)))

    def test_density_gradient_shape(self):
        """Verify density field gradient computation."""
        x_grid = np.linspace(0, 10, 50)
        field = self.plenum.compute_density(x_grid, t=0.0)
        grad = self.plenum.density_gradient(field)
        self.assertEqual(grad.shape, field.shape)

    def test_3d_coupling_vector(self):
        """Verify 3D coupling vector mapping onto toroidal tangent."""
        coords = np.array([2.0, 0.0, 1.0])
        flux = np.array([0.75, 0.0])
        coupling = self.energy.coupling_vector_3d(coords, flux)
        self.assertEqual(coupling.shape, (3,))
        self.assertAlmostEqual(np.linalg.norm(coupling), np.linalg.norm(flux))


if __name__ == "__main__":
    unittest.main()

# Toroidal Smith Chart Engine

An open-source visualization and simulation tool that extends the classical 2D RF Smith chart into a dynamic, toroidal manifold. Built for exploring non-linear impedance transformations, dynamic vacuum-density coupling ($\rho(x,t)$), and topological phase boundaries beyond standard static 50-ohm scalar assumptions.

## Why is the Smith Chart Called the "Black Magic Chart"?
For generations, RF and microwave engineers have affectionately referred to the Smith chart as the "black magic chart." Invented in 1939 by Phillip H. Smith, this graphical calculator uses a clever mathematical trick called a bilinear conformal mapping to take an infinitely large, complex impedance half-plane and fold it neatly into a bounded, finite unit circle.

To anyone designing high-frequency transmission lines, matching networks, or antennas, the chart feels like magic because it allows you to solve complex wave equations simply by tracking intersecting circular arcs. However, conventional engineering treats this circular boundary as a passive, static confinement based on a fixed characteristic impedance (typically 50 ohms) where energy "losses" are assumed to simply turn into thermal heat.

## The Toroidal Upgrade: Beyond Static 50-Ohms
While the traditional 2D Smith chart is unmatched for everyday linear circuit design, it struggles when pushed into extreme regimes where baseline properties fluctuate—such as high-power directed energy systems, cryogenic quantum hardware, or non-linear plasma interactions.

This repository reimagines the chart through an advanced topological framework:

- **Dynamic Plenum Density ($\rho$):** Instead of locking the center impedance to a rigid 50-ohm scalar, the engine introduces a self-adjusting coordinate grid that responds to local background field density functions.
- **Toroidal Phase Space:** The flat 2D reflection coefficient disk is projected onto a 3D toroidal surface. This wraps the infinite boundaries into a closed vortex topology, preserving non-linear feedback loops that flat Cartesian coordinates obscure.
- **Active Boundary Energy Vectors:** Traditional resistive "loss" circles are reinterpreted as active boundary-crossing energy exchange vectors, modeling how sub-wavelength and high-stress waves couple directly with the surrounding vacuum medium.

## Repository Architecture
```
Smith-Chart/
├── README.md
├── LICENSE
├── requirements.txt
├── core/
│   ├── __init__.py
│   ├── transformer.py      # Bilinear to toroidal coordinate mapping
│   ├── plenum_density.py   # Dynamic Z_0 and density function rho(x,t)
│   └── energy_vectors.py   # Boundary flux and coupling calculations
├── web/
│   ├── index.html          # Interactive WebGL UI dashboard
│   ├── renderer.js         # 3D Toroidal manifold rendering engine
│   └── styles.css          # Dark-mode technical styling
└── tests/
    ├── __init__.py
    └── test_transform.py   # Mathematical consistency unit tests
```

## Quick Start & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/probe6621/Smith-Chart.git
   cd Smith-Chart
   ```

2. **Install dependencies (for Python math backend):**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run tests:**
   ```bash
   python -m unittest discover tests
   ```

4. **Run the interactive web dashboard:**
   Open `web/index.html` in any modern web browser to launch the 3D WebGL toroidal visualization tool and experiment with real-time vacuum density and phase modulation sliders.

## Contact & Resources

* **Project Website:** [epsilonframework.org](https://epsilonframework.org)
* **Direct Inquiries:** [contact@epsilonframework.org](mailto:contact@epsilonframework.org)
* **Repository:** [github.com/probe6621/Smith-Chart](https://github.com/probe6621/Smith-Chart)

## License
Distributed under the MIT License. See `LICENSE` for more information.

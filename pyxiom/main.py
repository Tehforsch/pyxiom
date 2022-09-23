from pathlib import Path
from pyxiom.simulation import Simulation

sim = Simulation(Path("data"))
print(sim.output_files())

import sys
from pathlib import Path
import matplotlib.pyplot as plt
from pyxiom.simulation import Simulation

sim = Simulation(Path(sys.argv[1]))
for snap in sim.snapshots():
    positions = snap.position()
    plt.xlim((-2e14, 2e14))
    plt.ylim((-2e14, 2e14))
    plt.scatter(positions[:, 0], positions[:, 1], s=1)
    picsPath = sim.path / Path("pics")
    picsPath.mkdir(exist_ok=True)
    plt.savefig(picsPath / snap.str_num)
    plt.clf()

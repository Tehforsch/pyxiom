import sys
from pathlib import Path
import matplotlib.pyplot as plt
from pyxiom.simulation import Simulation

sim = Simulation(Path(sys.argv[1]))
for snap in sim.snapshots():
    positions = snap.position()
    plt.scatter(positions[:, 0], positions[:, 1])
    plt.savefig(Path("pics") / snap.str_num)
    plt.clf()

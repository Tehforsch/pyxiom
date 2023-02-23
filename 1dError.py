import numpy as np
import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
from pyxiom.simulation import Simulation
from pyxiom.snapshot import Snapshot
import astropy.units as u
import math


def setMatplotlibStyle() -> None:
    file_path = Path(os.path.realpath(__file__))
    plt.style.use(Path(file_path).parent / "styles/plot.mlpstyle")


def get_label(sim: Simulation) -> str:
    delta_t = u.Quantity(sim.parameters.raw_values["timestep"]["max_timestep"])
    num_levels = sim.parameters.raw_values["sweep"]["num_timestep_levels"]
    return f"$\\Delta t$ = {delta_t.to(u.kyr)}, {num_levels}"


def get_linestyle(sim: Simulation) -> str:
    num_levels = sim.parameters.raw_values["sweep"]["num_timestep_levels"]
    if num_levels == 1:
        return "-"
    elif num_levels == 2:
        return "--"
    elif num_levels == 3:
        return "-."
    elif num_levels == 4:
        return ":"
    raise ValueError()


def get_color(sim: Simulation) -> str:
    delta_t = u.Quantity(sim.parameters.raw_values["timestep"]["max_timestep"])
    print(delta_t, math.ceil(delta_t / (2.5 * u.kyr)))
    delta_t = math.ceil(delta_t / (2.5 * u.kyr))
    if delta_t == 2:
        return "r"
    elif delta_t == 4:
        return "g"
    elif delta_t == 8:
        return "b"
    elif delta_t == 16:
        return "brown"
    raise ValueError()


def sorted_abundances(snap: Snapshot) -> u.Quantity:
    positions = snap.position()
    sorted_indices = np.argsort(positions[:, 0])
    abundances = snap.ionized_hydrogen_fraction()
    return abundances[sorted_indices]


# setMatplotlibStyle()
sims = [Simulation(Path(path)) for path in sys.argv[1:]]
reference = sims[0]
times = u.Quantity([snap.time() for snap in reference.snapshots()])
for sim in sims[1:]:
    print(f"comparing {sim.path} to {reference.path}")
    diffs = []
    for snap in sim.snapshots()[1:]:
        snap_ref = next(s for s in reference.snapshots()[1:] if s.time() == snap.time())
        abundances_ref = sorted_abundances(snap_ref)
        abundances = sorted_abundances(snap)
        positions = snap.position()
        epsilon = 1e-20
        diff = np.abs(abundances - abundances_ref)
        diff = np.mean(diff)
        diffs.append(diff)
    plt.plot(times[1:].to_value(u.Myr), diffs, marker=".", label=get_label(sim), linestyle=get_linestyle(sim), color=get_color(sim))

plt.xlabel("t [Myr]")
plt.ylabel("mean rel. Error")
plt.legend()

picsPath = sim.path.parent / Path("pics")
print(picsPath)
picsPath.mkdir(exist_ok=True)
plt.savefig(picsPath / "error")

plt.show()

from typing import Dict
import numpy as np
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import astropy.units as u
import os
from matplotlib.ticker import FormatStrFormatter
from pyxiom.simulation import Simulation


def setMatplotlibStyle() -> None:
    file_path = Path(os.path.realpath(__file__))
    plt.style.use(Path(file_path).parent / "styles/plot.mlpstyle")


setMatplotlibStyle()
byResolution: Dict[float, float] = {}

plt.xscale("log")
plt.yscale("log")

plt.xlabel("$\\Delta t [\\mathrm{kyr}]$")
plt.ylabel("rel. Error")

plt.gca().xaxis.set_major_formatter(FormatStrFormatter("%.0f"))

plt.ticklabel_format()

for sim in [Simulation(sys.argv[1] / Path(p)) for p in os.listdir(sys.argv[1]) if not "pics" in p]:
    errorOverTime = sim.get_timeseries("rtype_error")
    resolution, timestep_in_kyr, num_levels = [int(x) for x in sim.path.name.split("_")]
    errorOverTime = sim.get_timeseries("rtype_error")
    last10Myr = np.where(errorOverTime.time.to_value(u.Myr) > 60.0)
    mean = np.mean(errorOverTime.value[last10Myr])
    if resolution == 64:
        print(timestep_in_kyr, num_levels, mean)
        plt.plot(timestep_in_kyr, mean, marker="o", linestyle="None")

plt.xticks([1000, 2000, 4000])
plt.yticks([1e0, 1e-1, 1e-2])

picsPath = sim.path / ".." / "pics"
picsPath.mkdir(exist_ok=True)
plt.savefig(picsPath / "expansionError")
plt.show()
plt.clf()

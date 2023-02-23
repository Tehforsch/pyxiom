from typing import Callable
import numpy as np
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import astropy.units as u

from pyxiom.simulation import Simulation
from pyxiom.snapshot import Snapshot
from pyxiom.parameters.parameters import BoxSize


def getIonization(positions: u.Quantity, data: u.Quantity, center: u.Quantity, radius: u.Quantity) -> u.Quantity:
    shellWidth = 0.5 * u.kpc
    distanceToCenter = getDistanceToCenter(positions, center)
    insideShell = np.where((distanceToCenter > radius - shellWidth / 2) & (distanceToCenter < radius + shellWidth / 2))
    if insideShell[0].shape[0] == 0:
        print("No data points inside shell")
        return float("nan")
        # raise ValueError("No data points inside shell")
    return np.mean(1 - data[insideShell])


def getDistanceToCenter(positions: u.Quantity, center: u.Quantity) -> u.Quantity:
    return np.linalg.norm(positions - center, axis=1)


def getIonizationRadius(snapshot: Snapshot, box_size: BoxSize, val: float = 0.5) -> u.Quantity:
    positions = snapshot.position()
    fraction = snapshot.ionized_hydrogen_fraction()

    def valueFunction(radius: u.Quantity) -> u.Quantity:
        return getIonization(positions, fraction, box_size.center(), radius)

    return bisect(valueFunction, val, 0 * u.m, box_size.max_side_length() / np.sqrt(2.0), precision=0.00001)


def analyticalRTypeExpansion(t: u.Quantity, recombination_time: u.Quantity, stroemgren_radius: u.Quantity) -> u.Quantity:
    return (1 - np.exp(-t / recombination_time)) ** (1.0 / 3) * stroemgren_radius


def analyticalDTypeExpansion(t: u.Quantity, ci: u.Quantity, stroemgrenRadius: u.Quantity) -> u.Quantity:
    return stroemgrenRadius * ((1 + 7 / 4 * ci * t / stroemgrenRadius) ** (4.0 / 7.0)).decompose()


def bisect(
    valueFunction: Callable[[u.Quantity], u.Quantity],
    targetValue: u.Quantity,
    start: u.Quantity,
    end: u.Quantity,
    precision: float = 0.01,
    depth: int = 0,
) -> u.Quantity:
    """Find the x at which the monotonously growing function valueFunction fulfills valueFunction(x) = targetValue to a precision (in x) of precision. start and end denote the maximum and minimum possible x value"""
    position = (end + start) / 2
    if depth > 100:
        print("Failed to bisect")
        return position
    if (end - start) / (abs(end) + abs(start)) < precision:
        return position
    value = valueFunction(position)
    if value < targetValue:
        return bisect(valueFunction, targetValue, position, end, precision=precision, depth=depth + 1)
    else:
        return bisect(valueFunction, targetValue, start, position, precision=precision, depth=depth + 1)


sim = Simulation(Path(sys.argv[1]))

recombination_time = 122.4 * u.Myr
stroemgren_radius = 6.79 * u.kpc

times = np.array([]) * u.s
radii = np.array([]) * u.m
analytical = np.array([]) * u.m
for snap in sim.snapshots():
    times = np.append(times, snap.time())
    radii = np.append(radii, getIonizationRadius(snap, sim.parameters.box_size))
    analytical = np.append(analytical, analyticalRTypeExpansion(snap.time(), recombination_time, stroemgren_radius))

plt.plot(times.to_value(u.Myr), radii.to_value(u.kpc))
plt.plot(times.to_value(u.Myr), analytical.to_value(u.kpc))
picsPath = sim.path / Path("pics")
picsPath.mkdir(exist_ok=True)
plt.savefig(picsPath / snap.str_num)
plt.show()
plt.clf()

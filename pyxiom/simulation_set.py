from typing import *

from pyxiom.simulation import Simulation
from pathlib import Path
import os
import polars as pl


class SimulationSet(dict):
    def __init__(self, path: Path) -> None:
        super().__init__(getSimsFromFolder(path))
        print(self)

    def get_time_series(self, names: [str]):
        dfs = [sim.get_time_series(names) for (i, sim) in self.items()]
        s = pl.concat(dfs)
        return s

def stringIsInt(s: str) -> bool:
    try:
        _ = int(s)
        return True
    except ValueError:
        return False


def getSimsFromFolder(sim_set_folder: Path) -> Iterator[Simulation]:
    folders = [sim_set_folder / Path(folder) for folder in os.listdir(sim_set_folder) if stringIsInt(folder)]
    folders.sort(key=lambda x: str(x.stem))
    return ((folder.stem, Simulation(folder)) for folder in folders)

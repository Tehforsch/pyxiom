from typing import *

from pyxiom.simulation import Simulation
from pathlib import Path
import os


class SimulationSet(list):
    def __init__(self, path: Path) -> None:
        super().__init__(getSimsFromFolder(path))

    def get_time_series(self, names: [str]):
        # df = pl.DataFrame()
        dfs = [sim.get_time_series(name) for (i, sim) in enumerate(self) for name in names]
        print(dfs)

def stringIsInt(s: str) -> bool:
    try:
        _ = int(s)
        return True
    except ValueError:
        return False


def getSimsFromFolder(sim_set_folder: Path) -> Iterator[Simulation]:
    folders = [sim_set_folder / Path(folder) for folder in os.listdir(sim_set_folder) if stringIsInt(folder)]
    folders.sort(key=lambda x: int(str(x.stem)))
    return (Simulation(folder) for folder in folders)

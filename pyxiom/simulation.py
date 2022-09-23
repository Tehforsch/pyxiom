from typing import List
from pathlib import Path

from pyxiom import config
from pyxiom.parameters import read_parameters
from pyxiom.snapshot import Snapshot, get_snapshots_from_dir


class Simulation:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.parameters = read_parameters(path / config.PARAMETER_FILE_NAME)

    def snapshots(self) -> List[Snapshot]:
        return get_snapshots_from_dir(self.path / config.SNAPSHOTS_DIR_NAME)

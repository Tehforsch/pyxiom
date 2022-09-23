from typing import List

from pathlib import Path
from pyxiom import config
from pyxiom.parameters import read_parameters


class Simulation:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.parameters = read_parameters(path / config.PARAMETER_FILE_NAME)

    def output_path(self) -> Path:
        return self.path / self.parameters["output"]["path"]

    def output_files(self) -> List[Path]:
        return [f for f in self.path / self.parameters["output"]["path"].walk()]

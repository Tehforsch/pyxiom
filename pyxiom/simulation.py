from typing import List
import os
from pathlib import Path

from pyxiom import config
from pyxiom.parameters import read_parameters


class Simulation:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.parameters = read_parameters(path / config.PARAMETER_FILE_NAME)

    @property
    def output_path(self) -> Path:
        return self.path / self.parameters.output.output_dir

    def output_files(self) -> List[Path]:
        return [Path(f) for f in os.listdir(self.output_path)]

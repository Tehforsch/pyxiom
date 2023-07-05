from typing import List
from pathlib import Path
from polars import DataFrame

from pyxiom import config
from pyxiom.parameters import read_parameters
from pyxiom.snapshot import Snapshot, get_snapshots_from_dir
from pyxiom.time_series import read_time_series


class Simulation:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.parameters = read_parameters(path / config.PARAMETER_FILE_NAME)

    def output_folder(self):
        output_folder = self.parameters["output"].get("output_folder")
        if output_folder is None:
            output_folder = "output"
        return self.path / Path(output_folder)

    def snapshots(self) -> List[Snapshot]:
        return get_snapshots_from_dir(self.output_folder() / config.SNAPSHOTS_DIR_NAME)

    def get_time_series(self, name: str) -> DataFrame:
        return read_time_series(self.output_folder() / config.TIME_SERIES_DIR_NAME / f"{name}.hdf5", name)

    def __repr__(self) -> str:
        return str(self.path)

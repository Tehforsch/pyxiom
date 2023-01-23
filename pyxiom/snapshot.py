from typing import List
from pathlib import Path

import numpy as np
import astropy.units as u
import h5py

from pyxiom.utils import get_dirs, get_files
from pyxiom.config import LENGTH_SCALING_IDENTIFIER, TIME_SCALING_IDENTIFIER, MASS_SCALING_IDENTIFIER, SCALE_FACTOR_SI_IDENTIFIER, SNAPSHOT_FILE_NAME


class SnapshotFileInfo:
    def __init__(self, path: Path, str_num: str, str_rank: str):
        self.path = path
        self.str_num = str_num
        self.str_rank = str_rank
        self.num = int(str_num)
        self.rank = int(str_rank)


class Snapshot:
    def __init__(self, files: List[SnapshotFileInfo]) -> None:
        self.files = files
        self.str_num = files[0].str_num
        assert all(f.str_num == self.str_num for f in self.files)
        self.num = files[0].num
        assert all(f.num == self.num for f in self.files)

    def hdf5_files(self) -> List[h5py.File]:
        return [h5py.File(f.path, "r") for f in self.files]

    def position(self) -> u.Quantity:
        return self.read_dataset("position")

    def ionized_hydrogen_fraction(self) -> u.Quantity:
        return self.read_dataset("ionized_hydrogen_fraction")

    def velocity(self) -> u.Quantity:
        return self.read_dataset("velocity")

    def temperature(self) -> u.Quantity:
        return self.read_dataset("temperature")

    def mass(self) -> u.Quantity:
        return self.read_dataset("mass")

    def time(self) -> u.Quantity:
        return self.read_attr("time") * u.s

    def read_dataset(self, name: str) -> u.Quantity:
        files = self.hdf5_files()
        data = np.concatenate(tuple(f[name][...] for f in files))
        unit = self.read_unit_from_dataset(name, files[0])
        return unit * data

    def read_attr(self, name: str) -> u.Quantity:
        files = self.hdf5_files()
        return files[0].attrs[name]

    def read_unit_from_dataset(self, dataset_name: str, f: h5py.File) -> u.Quantity:
        dataset = f[dataset_name]
        unit = 1.0
        unit *= u.m ** dataset.attrs[LENGTH_SCALING_IDENTIFIER]
        unit *= u.s ** dataset.attrs[TIME_SCALING_IDENTIFIER]
        unit *= u.kg ** dataset.attrs[MASS_SCALING_IDENTIFIER]
        return unit * dataset.attrs[SCALE_FACTOR_SI_IDENTIFIER]


def get_snapshot_paths_from_output_files(output_files: List[Path]) -> List[Path]:
    return [path for path in output_files if is_snapshot_file(path)]


def get_snapshots_from_dir(path: Path) -> List[Snapshot]:
    snap_dirs = get_dirs(path)
    return sorted([get_snapshot_from_dir(snap_dir) for snap_dir in snap_dirs], key=lambda snap: snap.num)


def get_snapshot_from_dir(path: Path) -> Snapshot:
    snapshot_infos = [parse_snapshot_file_name(snap_file) for snap_file in get_files(path)]
    return Snapshot(snapshot_infos)


def parse_snapshot_file_name(path: Path) -> SnapshotFileInfo:
    snap_num = path.parent.stem
    rank_num = path.stem
    return SnapshotFileInfo(path, snap_num, rank_num)


def is_snapshot_file(path: Path) -> bool:
    return SNAPSHOT_FILE_NAME in path.stem

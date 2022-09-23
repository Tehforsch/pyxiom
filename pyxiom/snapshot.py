from typing import List, Dict
from pathlib import Path

import numpy as np
import astropy.units as u
import h5py

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

    def read_dataset(self, name: str) -> u.Quantity:
        files = self.hdf5_files()
        data = np.concatenate(tuple(f[name][...] for f in files))
        unit = self.read_unit_from_dataset(name, files[0])
        return unit * data

    def read_unit_from_dataset(self, dataset_name: str, f: h5py.File) -> u.Quantity:
        dataset = f[dataset_name]
        unit = 1.0
        unit *= u.m ** dataset.attrs[LENGTH_SCALING_IDENTIFIER]
        unit *= u.s ** dataset.attrs[TIME_SCALING_IDENTIFIER]
        unit *= u.kg ** dataset.attrs[MASS_SCALING_IDENTIFIER]
        return unit * dataset.attrs[SCALE_FACTOR_SI_IDENTIFIER]


def get_snapshot_paths_from_output_files(output_files: List[Path]) -> List[Path]:
    return [path for path in output_files if is_snapshot_file(path)]


def get_snapshots_from_output_files(output_files: List[Path]) -> List[Snapshot]:
    snap_paths = [path for path in output_files if is_snapshot_file(path)]
    snapshot_infos = [parse_snapshot_file_name(snap_path) for snap_path in snap_paths]
    snapshots_by_num: Dict[int, List[SnapshotFileInfo]] = {}
    for snap in snapshot_infos:
        paths = snapshots_by_num.get(snap.num)
        if paths is None:
            snapshots_by_num[snap.num] = [snap]
        else:
            snapshots_by_num[snap.num].append(snap)
    nums = sorted(list(snapshots_by_num.keys()))
    return [Snapshot(snapshots_by_num[num]) for num in nums]


def parse_snapshot_file_name(path: Path) -> SnapshotFileInfo:
    stem = path.stem
    assert SNAPSHOT_FILE_NAME in stem
    split = stem.split("_")
    snap_num = split[1]
    rank_num = split[2]
    return SnapshotFileInfo(path, snap_num, rank_num)


def is_snapshot_file(path: Path) -> bool:
    return SNAPSHOT_FILE_NAME in path.stem

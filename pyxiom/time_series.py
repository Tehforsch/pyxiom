from pathlib import Path
import numpy as np
import h5py
import astropy.units as u
import polars as pl
from polars import DataFrame

from pyxiom.snapshot import read_unit_from_dataset


class TimeSeries:
    def __init__(self, file_: h5py.File, name: str) -> None:
        self.name = name
        self.time = read_dataset(file_, "time")
        self.value = read_dataset(file_, self.name)


def read_dataset(file_: h5py.File, dataset_name: str) -> u.Quantity:
    data = np.array(file_[dataset_name][...])
    unit = read_unit_from_dataset(dataset_name, file_)
    return unit * data


def read_time_series(path: Path, name: str) -> DataFrame:
    with h5py.File(path, "r") as f:
        series = TimeSeries(f, name)
        df = DataFrame({"time": series.time.to(u.s), name: series.value})
        return df

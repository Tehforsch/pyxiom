from __future__ import annotations
from typing import Any, Type
from pathlib import Path
import yaml
import astropy.units as u


class Parameters:
    def __init__(self, raw_values: dict) -> None:
        self.raw_values = raw_values
        self.set_values()
        if type(self) == Parameters:
            self.simulation = self.get_sub_parameters(SimulationParameters, "simulation")
            self.output = self.get_sub_parameters(OutputParameters, "output")

    def get_sub_parameters(self, param_type: Type[Parameters], identifier: str) -> Any:
        sub_params = self.raw_values.get(identifier)
        if sub_params is None:
            return param_type({})
        else:
            return param_type(sub_params)

    def set_values(self) -> None:
        pass

    def __getitem__(self, k: str) -> Any:
        return self.raw_values[k]

    # This is here to allow setting new attributes from set_values
    def __setattr__(self, name: str, value: Any) -> None:
        object.__setattr__(self, name, value)


class SimulationParameters(Parameters):
    def set_values(self) -> None:
        self.timestep = u.Quantity(self["timestep"])


class OutputParameters(Parameters):
    def set_values(self) -> None:
        self.output_dir: str = self["output_dir"]


def read_parameters(path: Path) -> Parameters:
    with open(path, "r") as f:
        return Parameters(yaml.load(f, Loader=yaml.SafeLoader))

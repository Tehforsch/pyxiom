import h5py

from pyxiom.simulation import Simulation


class Snapshot:
    def from_simulation_and_num(self, sim: Simulation, num: int) -> None:
        self.files = [f for f in sim.output_files()]

    def hdf5_files(self) -> h5py.Files:
        return [h5py.File(filename, "r") for filename in self.files]

from pyxiom import *


@sim_set_plot
def ionization_fraction_over_time(sims: SimulationSet) -> None:
    sims.get_time_series(["hydrogen_ionization_volume_average"])

from pyxiom import *
import matplotlib.pyplot as plt
import seaborn as sns
import polars as pl 
import astropy.units as u


@sim_set_plot
def ionization_fraction_over_time(sims: SimulationSet) -> None:
    df = sims.get_time_series(["hydrogen_ionization_volume_average", "hydrogen_ionization_mass_average"])
    s_to_myr = (u.s / u.Myr * 1.0).to_value(u.dimensionless_unscaled)
    df = df.with_columns(pl.col("time") * s_to_myr)
    delta_t = pl.Series([u.Quantity(sims[s].parameters["sweep"]["max_timestep"]).to_value(u.Myr) for s in df["sim"]])
    df = df.with_columns(delta_t.alias("delta_t [Myr]"))
    delta_t = pl.Series([sims[s].parameters["sweep"]["num_timestep_levels"] for s in df["sim"]])
    df = df.with_columns(delta_t.alias("num_levels"))
    print(df)
    g = sns.relplot(
        data=df, x="time", y="hydrogen_ionization_volume_average", style="num_levels", hue="delta_t [Myr]", kind="line", linewidth=2, height=2, aspect=1.5, legend=True
    )
    g.tight_layout()
    plt.show()
    g = sns.relplot(
        data=df, x="time", y="hydrogen_ionization_mass_average", style="num_levels", hue="delta_t [Myr]", kind="line", linewidth=2, height=2, aspect=1.5, legend=True
    )
    g.tight_layout()
    plt.show()

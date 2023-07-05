# type: ignore
import yaml
import click
from pyxiom.simulation_set import SimulationSet
from pathlib import Path


def configure(ctx, param, filename):
    with open(filename, "r") as f:
        cfg = yaml.load(f, Loader=yaml.UnsafeLoader)
    ctx.default_map = cfg


@click.group()
@click.option(
    "-c",
    "--config",
    type=click.Path(dir_okay=False),
    callback=configure,
    is_eager=True,
    expose_value=False,
    help="Read plot config file",
    show_default=True,
)
def cli():
    pass


def sim_set_plot(f):
    @cli.command(f.__name__.replace("_", "-"))
    @click.argument("sims", type=Path)
    def wrapper(sims: Path, *args, **kwargs) -> None:
        return f(SimulationSet(sims), *args, **kwargs)
    return wrapper

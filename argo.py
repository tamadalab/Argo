from sre_parse import Verbose
import click
from cli import cli1, cli2, cli3


@click.command(
    cls=click.CommandCollection,
    sources=[cli1.cli1, cli2.cli2, cli3.cli3]
)
@click.pass_context
def cli(ctx):
    pass


if __name__ == '__main__':
    cli()

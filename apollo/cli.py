from importlib.metadata import version, PackageNotFoundError
from typing             import List

import click

from .math.main import main as math_cli


def pkg_version() -> str:
    try:
        current_version: str = version('apollo')
    except PackageNotFoundError:
        current_version: str = 'uknown'

    return current_version


@click.command()
@click.version_option(pkg_version(), prog_name='apollo')
def main() -> None:
    '''[APOLLO] CLI - Command Line Interface'''
    pass


@main.command()
@click.option('--sum', 'op', flag_value='sum', help='Sum all given numbers')
@click.option('--mean', 'op', flag_value='mean', help='Calculate the mean of all given numbers')
@click.option('--eval', 'op', flag_value='eval', help='Evaluate the expression (default)')
@click.argument('args', nargs=-1)
def math(op: str, args: List[str]) -> None:
    '''Perform math operations on given numbers'''
    try:
        result = math_cli(args, operation=op)
        click.echo(f'= {result}')
    except Exception as e:
        click.echo(f'Error: {e}', err=True)
from importlib.metadata import version, PackageNotFoundError
from typing             import List

import click

from . import math as _math
from . import webcam as _webcam


def pkg_version() -> str:
    try:
        current_version: str = version('apollo')
    except PackageNotFoundError:
        current_version: str = 'uknown'

    return current_version


@click.group()
@click.version_option(pkg_version(), prog_name='apollo')
def main() -> None:
    '''[APOLLO] CLI - Command Line Interface'''
    pass


@main.command()
@click.option('--sum', 'op', flag_value='sum', help='Sum all given numbers')
@click.option('--mean', 'op', flag_value='mean', help='Calculate the mean of all given numbers')
@click.option('--min', 'op', flag_value='min', help='Minimum value')
@click.option('--max', 'op', flag_value='max', help='Maximum value')
@click.option('--prod', 'op', flag_value='prod', help='Product of all values')
@click.option('--median', 'op', flag_value='median', help='Median value')
@click.option('--diff', 'op', flag_value='diff', help='Difference between consecutive elements')
@click.option('--sqrt', 'op', flag_value='sqrt', help='Square root of a single number')
@click.option('--log', 'op', flag_value='log', help='Natural logarithm of a single number')
@click.option('--exp', 'op', flag_value='exp', help='Exponential of a single number')
@click.option('--abs', 'op', flag_value='abs', help='Absolute value of a single number')
@click.option('--round', 'op', flag_value='round', help='Round a single number to the nearest integer')
@click.option('--eval', 'op', default=True, flag_value='eval', help='Evaluate the math expression (default)')
@click.argument('args', nargs=-1)
def math(op: str, args: List[str]) -> None:
    '''Perform math operations on given numbers'''
    try:
        result = _math.main(args, operation=op)
        click.echo(f'= {result}')
    except Exception as e:
        click.echo(f'Error: {e}', err=True)


@main.command()
@click.option('--cam', 'camera', default=0, help='Camera index', type=int)
def webcam(camera: int) -> None:
    '''Displays a live webcam feed as ASCII art in the terminal.'''
    _webcam.main(camera)
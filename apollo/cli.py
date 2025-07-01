# cli.py
# Command Line Interface

from __future__ import annotations

from importlib.metadata import version, PackageNotFoundError
from typing import List, Literal

import click

from . import math as _math
from . import ascii as _ascii
from . import download as _download
from .config import config as _config


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
@click.option('--shade', type=click.Choice(['solid', 'ascii', 'dot']), default='ascii', show_default=True, help='Shading style')
@click.option('--grayscale', '_grayscale', type=click.Choice(['mean', 'default']), default='default', show_default=True, help='Grayscale method')
@click.option('--cam', 'camera', type=int, default=0, show_default=True, help='Camera index')
def webcam(shade: str, _grayscale: str, camera: int) -> None:
    '''Displays a live webcam feed as ASCII art in the terminal.'''
    _ascii.webcam(shade, _grayscale, camera)


@main.command()
@click.argument('url')
@click.option('--output-path', default=None, help='Optional path to save the file')
@click.option('--res', default='best', type=click.Choice(['best', 'worst']), show_default=True, help='Video resolution')
@click.option('-o', '--open', is_flag=True, default=False, help='Open video after download')
def download(url: str, output_path: str, res: str, open: bool) -> None:
    '''Download youtube video from a given URL'''
    _download.download(url, output_path, res, open)


@main.command()
@click.option('--show', is_flag=True, help='Show a config parameter or all')
@click.option('--set', 'set_mode', is_flag=True, help='Set a config parameter')
@click.argument('parameter', required=False)
@click.argument('value', required=False)
def config(show: bool, set_mode: bool, parameter: str | None, value: str | None) -> None:
    '''View or update configuration.'''

    if show:
        _config.show(parameter)

    elif set_mode:
        if not parameter or not value:
            raise click.UsageError("You must provide both <parameter> and <value> with --set")
        _config.cset(parameter, value)

    else:
        raise click.UsageError("You must use either --show or --set")


@main.command()
@click.argument('url')
@click.option('--shade', type=click.Choice(['solid', 'ascii', 'dot']), default='ascii', show_default=True, help='Shading style')
@click.option('-d', '--delete', is_flag=True, default=False, help='Delete video after run')
def play(url: str, shade: str, delete: bool) -> None:
    '''Displays a youtube video as ASCII art in the terminal.'''
    _ascii.play(shade, url, delete)


@main.command()
@click.option('-a', type=float, default=.04, show_default=True, help='Rotation angle around X-axis')
@click.option('-b', type=float, default=.08, show_default=True, help='Rotation angle around Y-axis')
@click.option('--speed', type=float, default=.03, show_default=True, help='Rotation speed. Time between frames.')
def donut(a: float, b: float, speed: float) -> None:
    '''donut.c from www.a1k0n.net/2011/07/20/donut-math.html'''
    _ascii.donut(a, b, speed)
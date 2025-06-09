from importlib.metadata import version, PackageNotFoundError

import click


def pkg_version() -> None:
    try:
        current_version: str = version('apollo')
    except PackageNotFoundError:
        current_version: str = 'uknown'

    return current_version

@click.command()
@click.version_option(pkg_version(), prog_name='apollo')
def main() -> None:
    pass
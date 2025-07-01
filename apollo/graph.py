# graph.py
# Plot cartesian graphs into the terminal

from __future__ import annotations

import numpy as np, sys
import sys

from numpy.typing import NDArray
from typing import Protocol, Any, runtime_checkable
from warnings import warn


@runtime_checkable
class SuportsWrite(Protocol):
    def write(self, __s: str) -> object: ...


def resample(array: NDArray, target_len: int) -> NDArray:
    '''Resample an array to the given target length using interpolation.'''

    if len(array) == target_len: return array

    x_old: NDArray = np.linspace(0, 1, len(array))
    x_new: NDArray = np.linspace(0, 1, target_len)
    return np.interp(x_new, x_old, array)


def echo_graph(
    x: NDArray,
    y: NDArray,
    xattr: str | None = None,
    yattr: str | None = None,
    file: SuportsWrite | None = None,
    flush: bool = False
) -> None:

    '''Plots ascii cartesian grapth into a stream or sys.stdout (default)'''

    file = sys.stdout if file is None else file

    if not isinstance(file, SuportsWrite):
        raise TypeError('File must suport writing.')

    width, height = 80, 12

    if len(x) != len(y) or len(x) > width:
        x: NDArray = resample(x, width)
        y: NDArray = resample(y, width)

    x_norm = (x - np.min(x)) / (np.ptp(x) + 1e-8)
    y_norm = (y - np.min(y)) / (np.ptp(y) + 1e-8)

    x_scaled = (x_norm * (width  - 1)).astype(int)
    y_scaled = (y_norm * (height - 1)).astype(int)

    canvas: list = [[' ' for _ in range(width)] for _ in range(height)]

    for xi, yi in zip(x_scaled, y_scaled):
        row: int = height - 1 - yi
        canvas[row][xi] = '•'

    for row in canvas:
        file.write(''.join(row) + '\n')

    if flush:
        file.flush()


if __name__ == '__main__':
    x = np.linspace(0, 10, 50)
    y = np.sin(np.linspace(0, 10, 100))

    echo_graph(x, y)
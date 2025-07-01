# ascii.py
# Fun ASCII arts to prompt on the terminal

from __future__ import annotations

import numpy as np
import cv2
import sys
import os
import colorama

from cv2 import VideoCapture
from numpy.typing import NDArray
from typing import Literal

from .download import download


def echo(buffer: str, flush: bool = True) -> None:
    '''Faster than print'''
    sys.stdout.write(buffer)
    if flush: sys.stdout.flush()


def resize(img: NDArray, shape: tuple[int, int]) -> NDArray:
    return cv2.resize(img, shape, interpolation=cv2.INTER_AREA)


def get_ilum_idx(grayscale: NDArray, linspace_rgb: NDArray) -> NDArray:
    if linspace_rgb.size == 1: return 0
    diffs: NDArray = np.abs(grayscale[..., None] - linspace_rgb)
    return np.argmin(diffs, axis=-1)


def get_mean_grayscale(pixels: NDArray) -> NDArray:
    return pixels[..., :3].mean(axis=-1)


def get_grayscale(pixels: NDArray) -> NDArray:
    '''This functions is slightly slower then `get_mean_grayscale`,
    but giver more accurate results'''
    return np.dot(pixels[..., :3], [0.299, 0.587, 0.114])


def get_rgb_uint8(pixels: NDArray) -> tuple[NDArray]:
    r: NDArray = pixels[..., 2].astype(np.uint8)
    g: NDArray = pixels[..., 1].astype(np.uint8)
    b: NDArray = pixels[..., 0].astype(np.uint8)
    return r, g, b


def add_ansi(r: NDArray, g: NDArray, b: NDArray, chars: NDArray) -> NDArray:
    '''`(R, G, B) --> \\033[38;2;R;G;BmCHAR\\033[0m`'''
    # Ugly, but works
    ansi_prefix: NDArray = np.char.add(
        np.char.add(
            np.char.add(
                np.char.add(
                    np.char.add(
                        '\033[38;2;',           # --> \033[38;2;
                        r.astype(str)),         # --> \033[38;2;R
                    ';'),                       # --> \033[38;2;R;
                g.astype(str)),                 # --> \033[38;2;R;G
            ';'),                               # --> \033[38;2;R;G;
        b.astype(str))                          # --> \033[38;2;R;G;B
    ansi_prefix = np.char.add(ansi_prefix, 'm') # --> \033[38;2;R;G;Bm

    ansi_suffix: str = '\033[0m'

    return np.char.add(np.char.add(
                    ansi_prefix, chars),        # --> \033[38;2;R;G;BmCHAR
                           ansi_suffix)         # --> \033[38;2;R;G;BmCHAR\033[0m


def join(colored_chars: NDArray) -> str:
    return ('\033[H' + ''.join([''.join(row[::-1]) for row in colored_chars]))


def echo_video(
    shade: Literal['solid', 'ascii', 'dot'],
    _grayscale: Literal['mean', 'default'],
    camera: int = 0
) -> None:

    colorama.init()

    cap: VideoCapture = VideoCapture(camera)

    if not cap.isOpened():
        raise Exception('Could Not open the webcam')

    shades = \
    np.array(list(' _.,-=+;:cba!?0123456789$W#@Ñ')) if shade == 'ascii' else \
    np.array(list('█'))                             if shade == 'solid' else \
    np.array(list('•'))                             if shade == 'dot'   else None

    if shades is None:
        raise TypeError(f'{shade} if not a vaild shade type')

    os.system('cls' if os.name == 'nt' else 'clear')

    while True:
        ret, frame = cap.read()
        if not ret: break

        width, height = os.get_terminal_size()
        frame = cv2.flip(frame, 1)
        pixels: NDArray = resize(frame, (width, height))

        if _grayscale == 'mean': grayscale: NDArray = get_mean_grayscale(pixels)
        elif _grayscale == 'default': grayscale: NDArray = get_grayscale(pixels)

        linspace_rgb: NDArray = np.linspace(0, 255, len(shades), dtype=np.float32)
        indices: NDArray = get_ilum_idx(grayscale, linspace_rgb)
        chars: NDArray = shades[indices]

        r, g, b = get_rgb_uint8(pixels)

        colored_chars: NDArray = add_ansi(r, g, b, chars)
        output: str = join(colored_chars)

        echo(output)

    cap.release()
    os.system('cls' if os.name == 'nt' else 'clear')


webcam = echo_video


def play(shade: Literal['solid', 'ascii', 'dot'], url: str, delete: bool = True) -> None:
    if not os.path.exists(url):
        output_path: str = download(url=url, res='worst', output_path=None, open=False)
    else:
        output_path = url
    echo_video(shade, _grayscale='mean', camera=output_path)
    if delete: os.remove(output_path)

    os.system('cls' if os.name == 'nt' else 'clear')
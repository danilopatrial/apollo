# ascii.py
# Fun ASCII arts to prompt on the terminal

from __future__ import annotations

import numpy as np
import cv2
import sys
import os
import colorama
import math
import time

from math import cos, sin, pi
from cv2 import VideoCapture
from numpy.typing import NDArray
from typing import Literal

#from .download import download
def download(*args, **kwargs) -> None: ...


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


def donut(ai: float = .04, bi: float = .08, speed: float = .03) -> None:
    '''https://www.a1k0n.net/2011/07/20/donut-math.html'''

    width, height = os.get_terminal_size()

    theta_spacing: float = .07
    phi_spacing:   float = .02

    R1, R2, K2 = 1, 2, 5

    # Calculate K1 based on screen size: the maximum x-distance occurs
    # roughly at the edge of the torus, which is at x=R1+R2, z=0.  we
    # want that to be displaced 3/8ths of the width of the screen, which
    # is 3/4th of the way from the center to the side of the screen.
    # width*3/8 = K1*(R1+R2)/(K2+0)
    # width*K2*3/(8*(R1+R2)) = K1
    #K1: float = width * K2 * 3 / (8 * (R1 + R2)) - 15
    K1 = 25

    def render_frame(a: float, b: float) -> None:
        # precompute sines and cosines of A and B
        cosA: float = cos(a)
        sinA: float = sin(a)
        cosB: float = cos(b)
        sinB: float = sin(b)

        output:  list = [[' ' for _ in range(width)] for _ in range(height)]
        zbuffer: list = [[0.0 for _ in range(width)] for _ in range(height)]

        # theta goes around the cross-sectional circle of a torus
        for theta in np.arange(0, 2*pi, theta_spacing):

            # precompute sines and cosines of theta
            costheta: float = cos(theta)
            sintheta: float = sin(theta)

            # phi goes around the center of revolution of a torus
            for phi in np.arange(0, 2*pi, phi_spacing):

                # precompute sines and cosines of phi
                cosphi: float = cos(phi)
                sinphi: float = sin(phi)

                # the x,y coordinate of the circle, before revolving (factored
                # out of the above equations)
                circlex: float = R2 + R1 * costheta
                circley: float = R1 * sintheta

                # final 3D (x,y,z) coordinate after rotations, directly from
                # our math above
                x: float = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
                y: float = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
                z: float = K2 + cosA * circlex * sinphi + circley * sinA

                ooz: float = 1/z # 'one over' z

                # x and y projection. note that y is negated here, because y
                # goes up in 3D space but down on 2D displays.
                xprojection: int = int(width / 2 + K1 * ooz * x)
                yprojection: int = int(height / 2 - K1 * ooz * y)

                # calculate luminance.  ugly, but correct.
                luminance: float = cosphi * costheta * sinB - cosA * costheta * sinphi - \
                    sinA * sintheta + cosB * (cosA * sintheta - costheta * sinA * sinphi)

                # L ranges from -sqrt(2) to +sqrt(2). If it's < 0, the surface
                # is pointing away from us, so we won't bother trying to plot it.
                if not (luminance > 0):
                    continue

                if not (0 <= xprojection < width and 0 <= yprojection < height):
                    continue

                # test against the z-buffer. larger 1/z means the pixel is
                # closer to the viewer than what's already plotted.
                if not (ooz > zbuffer[yprojection][xprojection]):
                    continue

                zbuffer[yprojection][xprojection] = ooz
                luminance_index: int = int(luminance * 8)

                # luminance_index is now in the range 0..11 (8*sqrt(2) = 11.3)
                # now we lookup the character corresponding to the
                # luminance and plot it in our output:
                output[yprojection][xprojection] = '.,-~:;=!*#$@'[luminance_index]

        # now, dump output[] to the screen.
        # bring cursor to "home" location, in just about any currently-used
        # terminal emulation mode
        #os.system('cls' if os.name == 'nt' else 'clear')
        echo(''.join(''.join(row) for row in output))

    a, b = 0, 0
    while True:
        render_frame(a, b)
        a += ai
        b += bi

        time.sleep(speed)
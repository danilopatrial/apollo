import numpy as np
import cv2
import sys
import os
from colorama import init as colorama_init
from cv2 import VideoCapture, destroyAllWindows

colorama_init()

width, height = os.get_terminal_size()

shades = np.array(list(" _.,-=+;:cba!?0123456789$W#@Ñ"))
linspace_rgb = np.linspace(0, 255, len(shades), dtype=np.float32)

def get_ilum_index(grayscale: np.ndarray) -> np.ndarray:
    diffs = np.abs(grayscale[..., None] - linspace_rgb)
    return np.argmin(diffs, axis=-1)

def echo(pixels: np.ndarray) -> None:
    grayscale = pixels[..., :3].mean(axis=-1)
    indices = get_ilum_index(grayscale)
    chars = shades[indices]

    r = pixels[..., 2].astype(np.uint8)
    g = pixels[..., 1].astype(np.uint8)
    b = pixels[..., 0].astype(np.uint8)

    ansi_prefix = np.char.add(
        np.char.add(
            np.char.add(
                np.char.add(
                    np.char.add(
                        '\033[38;2;', 
                        r.astype(str)),
                    ';'),
                g.astype(str)),
            ';'),
        b.astype(str))
    ansi_prefix = np.char.add(ansi_prefix, 'm')

    ansi_suffix = '\033[0m'

    colored_chars = np.char.add(np.char.add(ansi_prefix, chars.astype(str)), ansi_suffix)

    output_lines = [''.join(row) for row in colored_chars]
    output = '\033[H' + '\n'.join(output_lines)

    sys.stdout.write(output)
    sys.stdout.flush()

def resize(img: np.ndarray, shape: tuple[int, int]) -> np.ndarray:
    return cv2.resize(img, shape, interpolation=cv2.INTER_AREA)

def main(camera: int = 0) -> None:
    cap = VideoCapture(camera)
    if not cap.isOpened():
        print('Could not open the webcam.')
        exit()

    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        ret, frame = cap.read()
        if not ret: break

        frame = cv2.flip(frame, 1)
        pixels = resize(frame, (width, height))
        echo(pixels)

    cap.release()
    destroyAllWindows()
import os
import numpy as np

from cv2 import VideoCapture, resize, waitKey, destroyAllWindows


width, height = os.get_terminal_size()


shades: np.ndarray = np.array(list(' _.,-=+;:cba!?0123456789$W#@Ñ'))
linspace_rgb: np.ndarray = np.linspace(0, 255, len(shades), dtype=np.float32)


def get_ilum_index(grayscale: np.ndarray) -> np.ndarray:
    diffs: np.ndarray = np.abs(grayscale[..., None] - linspace_rgb)
    return np.argmin(diffs, axis=-1)


def echo(pixels: np.ndarray) -> None:
    grayscale: np.ndarray = pixels[..., :3].mean(axis=-1)
    indices: np.ndarray = get_ilum_index(grayscale)
    output_arr: np.ndarray = shades[indices]
    output: str = ''.join(output_arr.flatten())
    print(output, end='', flush=True)


def main(camera: int = 0) -> None:
    cap: VideoCapture = VideoCapture(camera)
    if not cap.isOpened(): print('Could not open the webcam.'); exit()

    while True:
        ret, frame = cap.read()
        if not ret: break

        pixels: np.ndarray = resize(frame, (width, height))
        echo(pixels)

    cap.release()
    destroyAllWindows()
# file_manager.py
# File manager

from __future__ import annotations

from .config import config_path, get
import os
import sys
import shutil

def ls(dir: str, n: int) -> None:
    if n == 0: n = len(os.listdir(dir))
    for file in os.listdir(dir)[:n]:
        print(f'{file}')

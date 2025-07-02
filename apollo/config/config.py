# config/config.py
# Script to access config/config.json

from __future__ import annotations

import json
import os

from typing import Any


def show(parameter: str | None) -> None:
    exists()
    with open(json_path, 'r') as file:
        json_dict: dict = json.load(file)

    if parameter is None:
        print(json.dumps(json_dict, indent=2, ensure_ascii=False))

    elif parameter in json_dict:
        print(f'{parameter}: {json_dict[parameter]}')

    else:
        print(f'Parameter {parameter} not found.')


json_path = os.path.join('Apollo', 'apollo', 'config', 'config.json')

def exists() -> None:
    base_dict: dict = {'download-output-path': 'None'}

    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    if not os.path.isfile(json_path):
        with open(json_path, 'w', encoding='utf-8') as file:
            json.dump(base_dict, file, indent=2, ensure_ascii=False)


def get(parameter: str) -> Any:
    exists()
    with open(json_path, 'r') as file:
        json_dict: dict = json.load(file)

    if parameter not in json_dict:
        raise ValueError('Paramter not found.')

    return json_dict[parameter]


def cset(parameter: str, value: Any) -> None:
    exists()
    with open(json_path, 'r') as file:
        json_dict: dict = json.load(file)

    if parameter in json_dict:
        json_dict[parameter] = value

    else:
        print(f'Parameter {parameter} not found.')

    with open(json_path, 'w') as file:
        json.dump(json_dict, file, indent=2, ensure_ascii=False)
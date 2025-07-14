# config.py
# Script to access the config file

from __future__ import annotations

import json
import os

from typing import Any
from platformdirs import user_config_dir


config_dir = user_config_dir('apollo')
config_path = os.path.join(config_dir, 'config.json')

os.makedirs(config_dir, exist_ok=True)

if not os.path.exists(config_path):
    with open(config_path, 'w') as f:
        json.dump({"download-output-path": "None"}, f)

def show(parameter: str | None) -> None:
    with open(config_path, 'r') as file:
        json_dict: dict = json.load(file)

    if parameter is None:
        print(json.dumps(json_dict, indent=2, ensure_ascii=False))

    elif parameter in json_dict:
        print(f'{parameter}: {json_dict[parameter]}')

    else:
        print(f'Parameter {parameter} not found.')



def get(parameter: str) -> Any:
    with open(config_path, 'r') as file:
        json_dict: dict = json.load(file)

    if parameter not in json_dict:
        raise ValueError('Paramter not found.')

    return json_dict[parameter]


def cset(parameter: str, value: Any) -> None:
    with open(config_path, 'r') as file:
        json_dict: dict = json.load(file)

    if parameter in json_dict:
        json_dict[parameter] = value

    else:
        print(f'Parameter {parameter} not found.')

    with open(config_path, 'w') as file:
        json.dump(json_dict, file, indent=2, ensure_ascii=False)

import math
import numpy as np

from typing import Any, List, Dict, Callable
from itertools import chain


def main(*args: Any, operation: str = 'eval') -> float:
    args: List[str] = list(chain.from_iterable(args)) if isinstance(args[0], (list, tuple)) else list(args)

    if operation == 'eval':
        return float(eval(' '.join(args)))

    nums: List[float] = list(map(float, args))

    # operations that expect a list of values
    op_list: Dict[str, Callable[[List[float]], float]] = {
        'sum': sum,
        'mean': np.mean,
        'min': min,
        'max': max,
        'prod': np.prod,
        'median': np.median,
        'diff': lambda x: float(np.diff(x)[0]) if len(x) > 1 else 0.0
    }

    # operations that expect a single value
    op_single: Dict[str, Callable[[float], float]] = {
        'sqrt': math.sqrt,
        'log': math.log,
        'exp': math.exp,
        'abs': abs,
        'round': round
    }

    if operation in op_list:
        return float(op_list[operation](nums))
    elif operation in op_single:
        return float(op_single[operation](nums[0]))
    else:
        raise ValueError(f"Unsupported operation: {operation}")


import math
import numpy as np

from typing import Any, List, Dict, Callable


def main(*args: Any, operation: str = 'eval') -> float:

    if operation == 'eval': return eval(' '.join(args))

    args: List[float] = list(map(float, args))

    op_map: Dict[str, Callable[..., float]] = {
        'sum': sum,
        'mean': np.mean,
    }

    return op_map[operation](args)
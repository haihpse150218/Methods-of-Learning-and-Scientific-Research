"""D3. Backend Portability metrics (M3.1, M3.2).

M3.1 Cross-Backend StdDev: sigma(resolve rates across 3 backends)
M3.2 Min/Max Ratio: min(RR) / max(RR) across backends
"""

import numpy as np


def cross_backend_stddev(resolve_rates: dict[str, float]) -> float:
    """M3.1: Standard deviation of resolve rates across backends.

    Lower StdDev = more portable (harness works well regardless of backend).

    Args:
        resolve_rates: {backend_name: resolve_rate} e.g. {"claude": 0.70, "gpt": 0.65, "deepseek": 0.55}

    Returns:
        Float >= 0. Lower is better.
    """
    if len(resolve_rates) < 2:
        return 0.0
    rates = list(resolve_rates.values())
    return float(np.std(rates, ddof=0))


def min_max_ratio(resolve_rates: dict[str, float]) -> float:
    """M3.2: min(RR) / max(RR) across backends.

    Higher ratio = more portable. A ratio of 1.0 means perfect portability.
    A ratio of 0.5 means the worst backend achieves half of the best.

    Args:
        resolve_rates: {backend_name: resolve_rate}

    Returns:
        Float in [0, 1]. Returns 0.0 if max is 0.
    """
    if not resolve_rates:
        return 0.0
    rates = list(resolve_rates.values())
    max_rate = max(rates)
    min_rate = min(rates)
    if max_rate == 0:
        return 0.0
    return min_rate / max_rate

import os
import time
from functools import wraps


def configured_delay() -> float:
    try:
        return max(float(os.getenv("RATE_LIMIT_DELAY", "0")), 0.0)
    except ValueError:
        return 0.0


def rate_limit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        delay = configured_delay()
        if delay:
            time.sleep(delay)
        return func(*args, **kwargs)

    return wrapper

import time
import os
from functools import wraps

DELAY = float(os.getenv("RATE_LIMIT_DELAY", 5))

def rate_limit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        time.sleep(DELAY)
        return func(*args, **kwargs)
    return wrapper

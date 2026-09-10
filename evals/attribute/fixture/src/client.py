import time

def call_with_retry(fn, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return fn()
        except Exception:
            time.sleep(2 ** attempt)
    raise RuntimeError("exhausted retries")

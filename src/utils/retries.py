"""
Utility module for API resilience and error handling.
Implements exponential backoff to handle temporary API outages (e.g., 503 UNAVAILABLE or 429 TOO MANY REQUESTS).
"""

import time
from functools import wraps

def with_retries(max_retries: int = 3, base_delay: float = 2.0, max_delay: float = 10.0):
    """
    Decorator that applies exponential backoff for Gemini API calls.
    Only retries on 503 (Unavailable) or 429 (Too Many Requests).
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    error_msg = str(e)
                    
                    # Check if it is a rate limit or server overload error
                    if "503" in error_msg or "429" in error_msg or "UNAVAILABLE" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                        if retries == max_retries:
                            raise Exception(f"Gemini API is still overwhelmed after {max_retries} retries. Please try again in a few minutes.\nDetails: {error_msg}")
                        
                        # Exponential backoff calculation
                        delay = min(base_delay * (2 ** retries), max_delay)
                        print(f"API overload detected (503/429). Retrying in {delay} seconds... (Attempt {retries + 1}/{max_retries})")
                        time.sleep(delay)
                        retries += 1
                    else:
                        # Re-raise immediately if it's a structural error (e.g., 400 Bad Request, auth failure)
                        raise e
        return wrapper
    return decorator

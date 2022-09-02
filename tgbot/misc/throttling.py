throttling_rate_limit = 'throttling_rate_limit'
throttling_key = 'throttling_key'


def rate_limit(limit: int, key=None):
    def decorator(func):
        setattr(func, throttling_rate_limit, limit)
        if key:
            setattr(func, throttling_key, key)
        return func
    return decorator

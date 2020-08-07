import time
import hashlib
import pickle
from functools import wraps

cache = {}


def is_obsolete(entry, duration):
    d = time.time() - entry['time']
    return d > duration


def compute_key(function, args, kwargs):
    key = pickle.dumps((function.__name__ , kwargs))
    return hashlib.sha1(key).hexdigest()


def memoize(duration=10):
    def _memorize(function):
        @wraps(function)  # update_wrapper维持被修饰函数属性不变
        def __memorize(*args, **kwargs):
            key = compute_key(function, args, kwargs)

            if key in cache and not is_obsolete(cache[key], duration):
                print('we got a winner')
                return cache[key]['value']

            result = function(*args, **kwargs)
            cache[key] = {'value': result, 'time': time.time()}
            return result

        return __memorize

    return _memorize

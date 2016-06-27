SOME_CONST = 10


def cached(func):
    cache_dict = {}

    def wrapper(*args, **kwargs):
        key = str((func, args, kwargs))
        if key not in cache_dict:
            cache_dict[key] = func(*args, **kwargs)
        return cache_dict[key]

    return wrapper


if __name__ == "__main__":
    @cached
    def plus_some(x):
        return SOME_CONST + x

    print '10 + 5 =', plus_some(5)
    SOME_CONST = 100
    print '100 + 5 =', plus_some(5), '<= cache applied'

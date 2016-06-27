def file_parsed(filename, parser):
    def decorator(func):
        def wrapper():
            with open(filename) as f:
                for line in f:
                    args = parser(line)
                    yield func(args)
        return wrapper

    return decorator


def my_parser(line):
    return [int(x) for x in line.strip().split(',')]


@file_parsed('test.txt', my_parser)
def sum_muled_by_10(x):
    return sum(x) * 10


if __name__ == "__main__":
    for el in sum_muled_by_10():
        print el

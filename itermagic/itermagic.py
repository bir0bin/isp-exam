from Queue import Queue


def niter(s_iter, n=2):
    it = iter(s_iter)
    underlying_qs = [Queue() for _ in xrange(n)]

    def underlying_gen(q):
        while True:
            if q.empty():
                val = next(it)
                for it_q in underlying_qs:
                    it_q.put(val)
            yield q.get()

    return tuple(underlying_gen(q) for q in underlying_qs)


def merge_longer_iter(iters, fill):
    stop_iter_cnt = 0
    while True:
        resp = []
        for it in iters:
            try:
                val = next(it)
            except StopIteration:
                stop_iter_cnt += 1
                val = fill
            resp.append(val)
        if stop_iter_cnt < len(iters):
            yield tuple(resp)
            stop_iter_cnt = 0
        else:
            break


if __name__ == "__main__":
    arr = range(10)

    it1, it2 = niter(arr)
    next(it1)
    next(it1)

    for x in merge_longer_iter((it1, it2), 1337):
        print x

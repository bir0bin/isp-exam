from multiprocessing import Queue, Process, Value
from math import sqrt, floor


class WorkerProcess(Process):
    queue = None
    worker_id = 0
    exit_counter = None

    def __init__(self, wid, queue, exit_ctr):
        self.queue = queue
        self.worker_id = wid
        self.file = open('task{}.out'.format(wid), 'w')
        self.exit_counter = exit_ctr
        super(WorkerProcess, self).__init__()

    @staticmethod
    def _is_prime(num):
        num = num[0]
        for divisor in xrange(2, int(floor(sqrt(num))) + 1):
            if num % divisor == 0:
                return False
        return True

    @staticmethod
    def _even_count(args):
        a, b = args
        a, b = min(a, b), max(a, b)
        if a % 2 == 1 and b % 2 == 1:
            cnt = 0
        else:
            cnt = 1

        cnt += (b - a) / 2
        return cnt

    def run(self):
        while not self.queue.empty():
            task = self.queue.get()
            ret = ""
            if task['type'] == 'isprime':
                ret = str(self._is_prime(task['args']))
            elif task['type'] == 'counteven':
                ret = str(self._even_count(task['args']))
            self.file.write(str(task) + ": " + ret + "\n")
        self.file.close()
        with self.exit_counter.get_lock():
            self.exit_counter.value += 1


if __name__ == "__main__":
    import sys
    import time
    import ctypes
    if len(sys.argv) != 3:
        print 'Usage:', sys.argv[0], 'task_file.txt proc_cnt'
        sys.exit(0)
    q = Queue()
    pcount = int(sys.argv[2])
    with open(sys.argv[1]) as tfile:
        for line in tfile:
            task = line.split("\t")
            args = [int(x.strip()) for x in task[1].split(",")]
            q.put({'type': task[0].strip(), 'args': args})

    ex_ctr = Value(ctypes.c_int)
    for i in range(pcount):
        w = WorkerProcess(i + 1, q, ex_ctr)
        w.start()

    while ex_ctr.value != pcount:
        time.sleep(1)
    print 'Done'

import json
import time

class Job:

    def __init__(self, func, args, kw):
        self.started = time.time()
        self.func = func
        self.args = args
        self.kw = kw

    def show(self, now=None):
        if now is None:
            now = time.time()
        return "%s %ss %r %r %r" % (
            time.ctime(self.started), int(now-self.started),
            self.func, self.args, self.kw)

    __repr__ = show

class Running:

    def __init__(self):
        self.jobs = []

    def __iter__(self):
        return iter(self.jobs)

running = Running()

def run(func, *args, **kw):
    job = Job(func, args, kw)
    running.jobs.append(job)
    try:
        return func(*args, **kw)
    finally:
        running.jobs.remove(job)

def monitor(out):
    for j in running:
        out.write(repr(j)+'\n')

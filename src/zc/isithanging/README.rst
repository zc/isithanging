======================================================
A zc.monitor plugin for testing whether function hangs
======================================================

Somtimes, computation stops and it can be hard to find out why. Tools
like strace can be helpful, but are very low level. If a call hangs
calling external network services, all you might see is a select or
poll call and not what serveice was being called.

Isithanging provides a simple registry and a helper function for
registering and unregistering calls.  To illustrate how this, we'll
use a test function that blocks until we unblock it by setting an
event:

    >>> import zc.isithanging.tests
    >>> event, blocker = zc.isithanging.tests.create_blocker()

The blocker function just returns any arguments it was passed.

To check whether a function is blocking, we use ``zc.isinhanging.run`` to
run the function.  We'll do so here in a thread:

    >>> import zc.thread
    >>> @zc.thread.Thread
    ... def thread():
    ...     print zc.isithanging.run(blocker, 1, foo=2)

Let's create seome more jobs:

    >>> e1, b1 = zc.isithanging.tests.create_blocker()
    >>> @zc.thread.Thread
    ... def t1():
    ...     print zc.isithanging.run(b1, 1)
    >>> e2, b2 = zc.isithanging.tests.create_blocker()
    >>> @zc.thread.Thread
    ... def t2():
    ...     print zc.isithanging.run(b2, 2)

.. Give a little time for the threads to start:

    >>> import time; time.sleep(.01)

... Some time passes:

    >>> timetime += 1

We can see what's running by looking at ``zc.isithanging.running``:

    >>> now = time.time()
    >>> for r in zc.isithanging.running:
    ...     print r.show(now)
    Sun Nov 16 09:48:29 2014 1s <function f at 0x10251e500> (1,) {'foo': 2}
    Sun Nov 16 09:48:29 2014 1s <function f at 0x10251e9b0> (1,) {}
    Sun Nov 16 09:48:29 2014 1s <function f at 0x10251eb18> (2,) {}

The show function shows start time, elapsed time in seconds, function
and arguments.

... Some time passes:

    >>> timetime += 1

When a job stops, it's automatically unregistered:

    >>> e1.set(); t1.join()
    ((1,), {})

    >>> for r in zc.isithanging.running:
    ...     print r
    Sun Nov 16 09:48:29 2014 2s <function f at 0x102d1e500> (1,) {'foo': 2}
    Sun Nov 16 09:48:29 2014 2s <function f at 0x102d1eb18> (2,) {}

There's a zc.monitor command that prints the jobs:

    >>> import sys
    >>> zc.isithanging.isithanging(sys.stdout)
    Sun Nov 16 09:48:29 2014 2s <function f at 0x102d1e500> (1,) {'foo': 2}
    Sun Nov 16 09:48:29 2014 2s <function f at 0x102d1eb18> (2,) {}

Let's finish the jobs and try again:

    >>> event.set(); thread.join()
    ((1,), {'foo': 2})
    >>> e2.set(); t2.join()
    ((2,), {})

    >>> zc.isithanging.isithanging(sys.stdout)


=======
Changes
=======

0.1.0 (yyyy-mm-dd)
==================

Initial release

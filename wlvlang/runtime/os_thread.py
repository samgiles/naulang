"""
Thread support based on OS-level threads.


Duplicated and altered from the pypy repository
"""

import os
from rpython.rlib import rthread

# Here are the steps performed to start a new thread:
#
# * The bootstrapper.lock is first acquired to prevent two parallel
#   starting threads from messing with each other's start-up data.
#
# * The start-up data (the app-level callable and arguments) is
#   stored in the global bootstrapper object.
#
# * The new thread is launched at RPython level using an rffi call
#   to the C function RPyThreadStart() defined in
#   translator/c/src/thread*.h.  This RPython thread will invoke the
#   static method bootstrapper.bootstrap() as a call-back.
#
# * As if it was a regular callback, rffi adds a wrapper around
#   bootstrap().  This wrapper acquires and releases the GIL.  In this
#   way the new thread is immediately GIL-protected.
#
# * As soon as the GIL is acquired in the new thread, the gc_thread_run()
#   operation is called (this is all done by gil.after_external_call(),
#   called from the rffi-generated wrapper).  The gc_thread_run()
#   operation will automatically notice that the current thread id was
#   not seen before, and (in shadowstack) it will allocate and use a
#   fresh new stack.  Again, this has no effect in asmgcc.
#
# * Only then does bootstrap() really run.  The first thing it does
#   is grab the start-up information (app-level callable and args)
#   out of the global bootstrapper object and release bootstrapper.lock.
#   Then it calls the app-level callable, to actually run the thread.
#
# * After each potential thread switch, as soon as the GIL is re-acquired,
#   gc_thread_run() is called again; it ensures that the currently
#   installed shadow stack is the correct one for the currently running
#   thread.
#
# * Just before a thread finishes, gc_thread_die() is called to free
#   its shadow stack.  This has no effect in asmgcc.


class Bootstrapper(object):
    "A global container used to pass information to newly starting threads."

    # Passing a closure argument to rthread.start_new_thread() would be
    # theoretically nicer, but comes with messy memory management issues.
    # This is much more straightforward.

    nbthreads = 0

    # The following lock is held whenever the fields
    # 'bootstrapper.rpy_callable' and 'bootstrapper.args' are in use.
    lock = None
    args = ()
    rpy_callable = None

    @staticmethod
    def setup():
        if bootstrapper.lock is None:
            try:
                bootstrapper.lock = rthread.allocate_lock()
            except rthread.error:
                raise Exception("can't allocate bootstrap lock")

    @staticmethod
    def reinit():
        bootstrapper.lock = None
        bootstrapper.nbthreads = 0
        bootstrapper.rpy_callable = None
        bootstrapper.args = ()

    def _cleanup_(self):
        self.reinit()

    def bootstrap():
        # Note that when this runs, we already hold the GIL.  This is ensured
        # by rffi's callback mechanism: we are a callback for the
        # c_thread_start() external function.
        rthread.gc_thread_start()
        print "In Thread"
        space = bootstrapper.space
        rpy_callable = bootstrapper.rpy_callable
        args = bootstrapper.args
        bootstrapper.nbthreads += 1
        bootstrapper.release()
        # run!
        try:
            print "Running the code"
            bootstrapper.run(space, rpy_callable, args)
            # done
        except Exception, e:
            # oups! last-level attempt to recover.
            try:
                STDERR = 2
                os.write(STDERR, "Thread exited with ")
                os.write(STDERR, str(e))
                os.write(STDERR, "\n")
            except OSError:
                pass
        bootstrapper.nbthreads -= 1
        rthread.gc_thread_die()
    bootstrap = staticmethod(bootstrap)

    def acquire(space, rpy_callable, args):
        if bootstrapper.lock is None:
            bootstrapper.setup()

        # If the previous thread didn't start yet, wait until it does.
        # Note that bootstrapper.lock must be a regular lock, not a NOAUTO
        # lock, because the GIL must be released while we wait.
        bootstrapper.lock.acquire(True)
        print "Acquired lock"
        bootstrapper.space = space
        bootstrapper.rpy_callable = rpy_callable
        bootstrapper.args = args
    acquire = staticmethod(acquire)

    def release():
        # clean up 'bootstrapper' to make it ready for the next
        # start_new_thread() and release the lock to tell that there
        # isn't any bootstrapping thread left.
        bootstrapper.rpy_callable = None
        bootstrapper.args = ()
        print "Releasing lock"
        bootstrapper.lock.release()
    release = staticmethod(release)

    def run(space, rpy_callable, args):
        rpy_callable.run(args, space)

    run = staticmethod(run)

bootstrapper = Bootstrapper()
Bootstrapper.setup()

def start_new_thread(space, rpy_callable, args, w_kwargs=None):
    """Start a new thread and return its identifier.  The thread will call the
function with positional arguments from the tuple args and keyword arguments
taken from the optional dictionary kwargs.  The thread exits when the
function returns; the return value is ignored.  The thread will also exit
when the function raises an unhandled exception; a stack trace will be
printed unless the exception is SystemExit."""
    bootstrapper.acquire(space, rpy_callable, args)
    try:
        ident = rthread.start_new_thread(bootstrapper.bootstrap, ())
    except Exception, e:
        bootstrapper.release()     # normally called by the new thread
        raise e

    return ident


def get_ident(space):
    """Return a non-zero integer that uniquely identifies the current thread
amongst other threads that exist simultaneously.
This may be used to identify per-thread resources.
Even though on some platforms threads identities may appear to be
allocated consecutive numbers starting at 1, this behavior should not
be relied upon, and the number should be seen purely as a magic cookie.
A thread's identity may be reused for another thread after it exits."""
    return rthread.get_ident()

def stack_size(space, size=0):
    """stack_size([size]) -> size

Return the thread stack size used when creating new threads.  The
optional size argument specifies the stack size (in bytes) to be used
for subsequently created threads, and must be 0 (use platform or
configured default) or a positive integer value of at least 32,768 (32k).
If changing the thread stack size is unsupported, a ThreadError
exception is raised.  If the specified size is invalid, a ValueError
exception is raised, and the stack size is unmodified.  32k bytes
is currently the minimum supported stack size value to guarantee
sufficient stack space for the interpreter itself.

Note that some platforms may have particular restrictions on values for
the stack size, such as requiring a minimum stack size larger than 32kB or
requiring allocation in multiples of the system memory page size
- platform documentation should be referred to for more information
(4kB pages are common; using multiples of 4096 for the stack size is
the suggested approach in the absence of more specific information)."""
    raise Exception("setting stack size not supported")

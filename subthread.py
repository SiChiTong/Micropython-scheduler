# subthread.py Demo/test  of one thread starting another and receiving a result from it
# Author: Peter Hinch
# V1.02 6th Sep 2014

from usched import Sched, Roundrobin, wait

# Run on MicroPython board bare hardware
# THREADS:

def subthread(lstResult):                                   # Gets a list for returning result(s) to caller
    yield Roundrobin()
    print("Subthread started")                              # In this test list simply contains a boolean
    yield from wait(1)
    print("Subthread end")
    lstResult[0] = True

def waitforit(objSched):                                    # Waits forever on subthread. Could readily wait on more than one thread.
    result = [False]                                        # Result array will be changed by subthread before it terminates
    print("Waiting on thread")
    objSched.add_thread(subthread(result))
    while not result[0]:                                    # Subthread will set element 0 True on completion
        yield Roundrobin()                                  # In a useful application would return other results too
    print("Thread returned")

# USER TEST PROGRAM
# Runs to completion and terminates because all threads have ended
def test():
    print("Demonstration of subthreads")
    objSched = Sched()
    objSched.add_thread(waitforit(objSched))                 # Test of one thread waiting on another
    objSched.run()

test()


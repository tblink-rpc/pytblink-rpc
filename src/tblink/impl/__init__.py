#****************************************************************************
#* tblink.impl package
#****************************************************************************
import asyncio
import importlib
import os
import sys

_is_running = False

def init(a, b):
    print("a=" + str(a) + " b=" + str(b))
    # Prefix the path with 'impl' so we find the tblink cocotb package first
    impl_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, impl_dir)
    
    print("tblink.impl.start()")
    
    if "MODULE" not in os.environ.keys():
        raise Exception("MODULES not set")
   
    print("Loading module: " + os.environ["MODULE"])
    try:
        m = importlib.import_module(os.environ["MODULE"])
    except Exception as e:
        print("Exception: " + str(e))
        raise e

async def entry_wrapper(entry_f):
    global _is_running
    print("entry_wrapper: " + str(entry_f))
    _is_running = True
    
    try:
        await entry_f(None)
    except Exception as e:
        print("Exception from entry: " + str(e))
    _is_running = False

def entry():
    global _is_running
    print("--> entry()")
    _is_running = True
    try:
        loop = asyncio.get_event_loop()
        entry_f = TestRgy.inst().tests[0]
        print("entry_f: " + str(entry_f))
        t = asyncio.ensure_future(entry_wrapper(entry_f))
        print("  t=" + str(t))
    except Exception as e:
        print("Exception: " + str(e))
        raise e
            
    print("<-- entry()")
    pass

def __end_reschedule(loop):
    """Allows us to stop the event loop after processing all pending events"""
    print("_end_reschedule")
    loop.stop()

def reschedule():
    """Runs the event loop to handle task updates"""
    global _is_running
    print("reschedule")
    loop = asyncio.get_event_loop()

    # Skip running the event loop if the main
    # coroutine has terminated    
    if not _is_running:
        return

#    f = loop.create_future()
    
    # Callback after all active tasks have settled
    print("--> Calling run_forever")
    loop.call_soon(__end_reschedule, loop)
    loop.run_forever()
    print("<-- Calling run_forever")
    
    return _is_running

    
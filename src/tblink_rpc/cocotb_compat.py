#****************************************************************************
#* cocotb_compat.py
#****************************************************************************
import re
import sys
import traceback

import cocotb

from tblink_rpc.impl.backend_cocotb import BackendCocotb
from tblink_rpc.impl.iftype_rgy import IftypeRgy
from tblink_rpc_core.endpoint import comm_mode_e, comm_state_e
from tblink_rpc.tblink import TbLink


_ifinsts = []
_debug = False

def ifinsts():
    global _ifinsts
    return _ifinsts

def find_ifinst(name, cls=None):
    matches = find_ifinsts(name, cls)
    
    if len(matches) == 0:
        raise Exception("No instances matched %s" % name)
    elif len(matches) > 1:
        raise Exception("Multiple instances matched %s" % name)
    
    return matches[0]

def find_ifinsts(name, cls=None):
    global _ifinsts

    name_p = re.compile(name)
    
    matches = []
    for i in _ifinsts:
        if name_p.match(i.inst_name()):
            print("matches")
            if cls is None or type(i) == cls:
                matches.append(i)
    
    return matches

async def init():
    try:
        await _init()
    except Exception as e:
        print("TbLink cocotb: %s" % str(e), flush=True)
        traceback.print_exc()
        sys.stdout.flush()
        raise e
    
async def _init():
    global _ifinsts
    tblink = TbLink.inst()
   
    # Configure TbLink to use cocotb's event class 
#    tblink.mk_ev = _mk_ev

    # Don't know precisely the order in 
    # which Cocotb and TbLink will be loaded.
    #
    # Spin for a few deltas waiting for the
    # default endpoint to register
    for i in range(16):
        dflt = tblink.getDefaultEP()
        if dflt is not None:
            print("Python: Found default EP", flush=True)
            break
        else:
            print("Python: Waiting for default EP", flush=True)
            await cocotb.triggers.Timer(0, 'ns')
            
    if dflt is None:
        raise Exception("TbLink Error: no default endpoint is registered")
    
    # TODO: Use 'launcher' to connect to the existing endpoint
    launcher = tblink.findLaunchType("connect.native.loopback")
    params = launcher.newLaunchParams()
    ep,err = launcher.launch(params)
    
    if ep is None:
        raise Exception("Failed to connect: %s" % err)
    
    ep.init(None)
    
    ev = cocotb.triggers.Event()
    
    def event_l(e):
        nonlocal ev
        print("Python Main: event %s" % str(ev))
        ev.set()
    
    l = ep.addListener(event_l)

    print("--> Python is_init", flush=True)
    while True:
        ret = ep.is_init()
        
        if ret == 1:
            break
        elif ret == -1:
            raise Exception("Failed during init")
        else:
            print("--> init: ev.wait", flush=True)
            await ev.wait()
            ev.clear()
            print("<-- init: ev.wait", flush=True)
    print("<-- Python is_init", flush=True)
            

    # TODO: Register BFM types with the endpoint

    # TODO: not the best name...    
    IftypeRgy.inst().endpoint_added(ep)
    
    print("Registered Types")
    for iftype in ep.getInterfaceTypes():
        print("iftype: %s" % iftype.name())

    # TODO: Complete build stage. This ensures we know about all peer-registered instances
    if ep.build_complete() == -1:
        raise Exception("Build-complete failed")
    
    for _ in range(10):
        print("--> is_build_complete", flush=True)
        code = ep.is_build_complete()
        print("<-- is_build_complete %d" % code, flush=True)
        if code == 0:
            print("--> process_one_message_a: is_build_complete", flush=True)
            await ev.wait()
            ev.clear()
            print("<-- process_one_message_a: is_build_complete", flush=True)
#            await cocotb.triggers.Timer(0, 'ns')
#            ep.add_time_callback(0, delta_cb)
#            await ev.wait()
#            ev.clear()
#            ep.process_one_message()
        elif code == -1:
            raise Exception("Is-build-complete failed")
        else:
            break
        
    if ep.is_build_complete() != 1:
        raise Exception("TbLink-RPC cocotb: Time-out during is-build-complete")
    else:
        print("Python BUILD_COMPLETE", flush=True)
    
    # << User calls library 'init'

    # At this point, we know what BFMs exist in the HDL environment
    # Use the Python facade to construct user-specified classes
    print("--> build_bfms", flush=True)
    backend = BackendCocotb(ep)
    tblink = TbLink.inst()
    tblink.dflt_backend = backend
    bfms = IftypeRgy.inst().build_bfms(backend)
    print("<-- build_bfms", flush=True)
    _ifinsts.extend(bfms)

    print("Python: dflt=%s" % str(dflt), flush=True)    
    
    print("--> Python connect_complete")
    if ep.connect_complete() == -1:
        raise Exception("Connect-complete failed")
    print("<-- Python connect_complete")
    
    while True:
        print("--> is_connect_complete", flush=True)
        code = ep.is_connect_complete()
        print("<-- is_connect_complete %d" % code, flush=True)
        if code == 0:
            print("--> process_one_message_a: is_connect_complete")
            await ev.wait()
            ev.clear()
#            await ep.process_one_message_a()
            print("<-- process_one_message_a: is_connect_complete")
#            await cocotb.triggers.Timer(0, 'ns')
#            ep.process_one_message()
        elif code == -1:
            raise Exception("Is-connect-complete failed")
        else:
            break
        
    ep.removeListener(l)

    # << User calls library 'complete'
    
    # Release the endpoint, allowing cocotb to control
    # and gate simulation
    
    print("--> update_comm_mode", flush=True)
    try:
        ep.update_comm_mode(comm_mode_e.Explicit, comm_state_e.Released)
    except Exception as e:
        print("Exception: %s" % str(e))
        traceback.print_exc()
    print("<-- update_comm_mode", flush=True)
    
    pass


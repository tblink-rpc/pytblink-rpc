'''
Created on Jan 21, 2022

@author: mballance
'''

import tblink_rpc
from tblink_rpc.tblink import TbLink
from tblink_rpc_core.endpoint import EndpointFlags
import sys
import os
import importlib
import traceback
from tblink_rpc.rt.cocotb.mgr import Mgr

def main():
    tblink = TbLink.inst()
    
    # cocotb has a native module for interfacing with the 
    # simulator. We need to provide our own cocotb 'simulator'
    # module. We do this by inserting our own module prior
    # to importing cocotb.
    sys.modules['cocotb.simulator'] = importlib.import_module("tblink_rpc.rt.cocotb.simulator")
    

    target_ep = None
    for ep in tblink.getEndpoints():
        flags = ep.getFlags()
        print("ep=%s flags=%s" % (str(ep), str(flags)), flush=True)
        if EndpointFlags.LoopbackSec in flags and EndpointFlags.Claimed not in flags:
            target_ep = ep
            break

    if target_ep is None:
        raise Exception("Failed to find loopback endpoint to connect to")
    
    target_ep.setFlag(EndpointFlags.Claimed)        
    print("target_ep: %s" % str(target_ep), flush=True)

    # Set the endpoint for when the user calls    
    # Note: it's required to import the module here so as
    # to avoid messing up replacement of the simulator module
    from tblink_rpc import cocotb_compat
    cocotb_compat._set_ep(target_ep)
    
    mgr = Mgr.inst()
    mgr.ep = target_ep
    
    try:
        import cocotb
        cocotb._initialise_testbench([])
    except Exception as e:
        print("Exception: %s" % str(e), flush=True)
        traceback.print_exc()
            
    pass

if __name__ == "__main__" or __name__.endswith(".__main__"):
    try:
        main()
    except Exception as e:
        print("Exception in main: %s" % str(e), flush=True)

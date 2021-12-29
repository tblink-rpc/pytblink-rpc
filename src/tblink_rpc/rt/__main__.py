'''
Created on Mar 29, 2021

@author: mballance
'''
import argparse
import asyncio
import os
import sys
import traceback

from tblink_rpc.rt.endpoint_sequencer import EndpointSequencer
from tblink_rpc_core.endpoint import Endpoint
from tblink_rpc.tblink import TbLink
import tblink_rpc_core
from tblink_rpc.rt.backend_asyncio import BackendAsyncio
from tblink_rpc.impl.iftype_rgy import IftypeRgy


def getparser():
    parser = argparse.ArgumentParser()
    
    return parser

_seqr = None

def main():
    global _seqr
    
    print("Hello")

    tblink = TbLink.inst()
    tblink.tblink_core = tblink_rpc_core.tblink.TbLink.inst()
    
    ep : Endpoint = None
    err = ""
    is_async = False

    # Determine what integration is being used
    if "TBLINK_PORT" in os.environ.keys():
        # We're running remote
        print("TbLink Note: Running in remote-process mode")
        launch_t = tblink.findLaunchType("connect.socket")
        params = launch_t.newLaunchParams()
        params.add_param("port", os.environ["TBLINK_PORT"])
        params.add_param("host", os.environ["TBLINK_HOST"])
        ep,err = launch_t.launch(params, None)
        print("ep=%s ; err=%s" % (str(ep), str(err)), flush=True)
        print("launch_t=%s" % str(launch_t), flush=True)
    else:
        # We're running as loopback
        print("TbLink Note: Running in loopback mode")
        launch_t = tblink.findLaunchType("connect.loopback")
        params = launch_t.newLaunchParams()
        ep,err = launch_t.launch(params, None)
        
        # With loopback, we expect to receive messages
        # asynchronously.
        pass
    
    if ep is None:
        raise Exception("Failed to launch endpoint: %s" % err)
    
    tblink.dflt_backend = BackendAsyncio(ep)
    
    ep.init(None)
    _seqr = EndpointSequencer(ep, tblink.dflt_backend, is_async)

    try:    
        _seqr.run()
    except Exception as e:
        print("Exception: %s" % str(e), flush=True)
        sys.exit(1)
    pass

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Exception: %s" % str(e), flush=True)
        traceback.print_exc()
        
    print("Exiting Main", flush=True)
            

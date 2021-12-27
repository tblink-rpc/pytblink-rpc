'''
Created on Mar 29, 2021

@author: mballance
'''
import argparse
import asyncio
import sys
import os
from tblink_rpc_core.tblink import TbLink
import traceback
from tblink_rpc_core.endpoint import Endpoint

def getparser():
    parser = argparse.ArgumentParser()
    
    return parser

def main():
    print("Hello")
    
    tblink = TbLink.inst()
    
    ep : Endpoint = None
    err = ""

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
        
        for a in ep.args():
            print("Arg: %s" % str(a))
    else:
        # We're running as loopback
        print("TbLink Note: Running in loopback mode")
        pass
    pass

    if ep is None:
        raise Exception("")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Exception: %s" % str(e), flush=True)
        traceback.print_exc()
            

'''
Created on Mar 29, 2021

@author: mballance
'''
import argparse
import asyncio
import socket
import sys
import os
from tblink_rpc.runtime.socket_message_transport import SocketMessageTransport
import json
from tblink_rpc.runtime.initialize_req import InitializeReq

def getparser():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("host")
    parser.add_argument("port")
    
    return parser

def main():
    runtime_dir = os.path.dirname(os.path.abspath(__file__))
    tblink_dir = os.path.dirname(runtime_dir)
    
    args = [] 
    plusargs = []
    for a in sys.argv[1:]:
        if a.startswith("+"):
            plusargs.append(a)
        else:
            args.append(a)
    
    # Update the search path such that 'cocotb' is found 
    # here first
    sys.path.insert(0, os.path.join(tblink_dir, "impl"))
    
    parser = getparser()
    
    print("args=" + str(args))
    
    args = parser.parse_args(args)
    
    print("Hello from main: " + args.host + " " + args.port)
  
    reader,writer = asyncio.get_event_loop().run_until_complete(
        asyncio.open_connection(args.host, int(args.port)))
    
    print("reader=" + str(reader) + " writer=" + str(writer))

    transport = SocketMessageTransport(reader, writer)
     
    init = InitializeReq()

    msgloop_t = asyncio.ensure_future(transport.msgloop())
     
    asyncio.get_event_loop().run_until_complete(
        transport.send(init.dump()))
    
    print("--> run_forever")
    # Keep running as long as the event loop does
    # TODO: add in user test too
    asyncio.get_event_loop().run_until_complete(msgloop_t)
#    asyncio.get_event_loop().run_forever()
    print("<-- run_forever")


if __name__ == "__main__":
    main()

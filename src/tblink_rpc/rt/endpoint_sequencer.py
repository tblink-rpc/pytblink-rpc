'''
Created on Dec 27, 2021

@author: mballance
'''
import asyncio
from enum import Enum
import importlib
import traceback

from tblink_rpc.impl.iftype_rgy import IftypeRgy
from tblink_rpc.rt.runner import Runner
from tblink_rpc_core.endpoint import comm_mode_e, comm_state_e
from tblink_rpc_core.endpoint_listener import EndpointListener
from tblink_rpc_core.event_type_e import EventTypeE


class State(Enum):
    ProcessMessages = auto()

class EndpointSequencer(object):
    
    def __init__(self, ep, backend, is_async):
        self.ep = ep
        self.backend = backend
        self.ep.addListener(self.event)
        self.is_async = is_async
        self.runner = None
        self.pending_time_reqs = 0

    def run(self):
        code = 0        
        while True:
            print("--> is_init", flush=True)
            code = self.ep.is_init()
            print("<-- is_init=%d" % code, flush=True)
            
            if code == 0:
                print("--> process_one_message", flush=True)
                code = self.ep.process_one_message()
                print("<-- process_one_message=%d" % code, flush=True)
                if code == -1:
                    break
            else:
                break

        if code != 1:
            raise Exception("Initialization sequence failed")

        clsname = None        
        for a in self.ep.args():
            print("Arg: %s" % str(a))
            if a.startswith("+tblink.class="):
                clsname = a[len("+tblink.class="):]
                
        if clsname is None:
            raise Exception("no +tblink.class specified")
        
        last_dot = clsname.rfind('.')

        if last_dot == -1:
            raise Exception("Malformed classname: expect at least one dot")
        
        modname = clsname[0:last_dot]
        clsname = clsname[(last_dot+1):]
       
        mod = importlib.import_module(modname)
        
        print("mod: %s" % str(mod))
        cls = getattr(mod, clsname)
        print("cls: %s" % str(cls))
        
        try:
            cls_i = cls("root", None)
        except Exception as e:
            print("Execption: %s" % str(e), flush=True)
            raise e

        # Register all discovered types with the endpoint
        IftypeRgy.inst().endpoint_added(self.ep)
            
        # Run the build phase
        try:
            cls_i._do_build(self.backend, self.ep)
        except Exception as e:
            print("Exception during build: %s" % str(e))
            raise e
        
        if self.ep.build_complete() == -1:
            raise Exception("TbLink Error: build_complete failed")
        
        while True:
            code = self.ep.is_build_complete()
            if code == -1:
                raise Exception("TbLink Error: is_build_complete failed")
            elif code == 0:
                if self.ep.process_one_message() == -1:
                    raise Exception("TbLink Error: process_one_message error during is_build_complete")
            else:
                break
            
        try:
            cls_i._do_connect(self.ep)
        except Exception as e:
            print("Exception during connect: %s" % str(e), flush=True)
            traceback.print_exc()
            raise e
                    
        if self.ep.connect_complete() == -1:
            raise Exception("TbLink Error: connect_complete failed")
        
        while True:
            code = self.ep.is_connect_complete()
            if code == -1:
                raise Exception("TbLink Error: is_connect_complete failed")
            elif code == 0:
                if self.ep.process_one_message() == -1:
                    raise Exception("TbLink Error: process_one_message error during is_connect_complete")
            else:
                break
            
        try:
            cls_i._do_start()
        except Exception as e:
            print("Exception during start: %s" % str(e), flush=True)
            traceback.print_exc()
            raise e

        loop = asyncio.get_event_loop()
        def _end_reschedule():
            nonlocal loop
            print("-- _end_reschedule")
            loop.stop()
            
        last_pending_time_reqs = 0
        while True:
            loop.call_soon(_end_reschedule)
            loop.run_forever()
            
            if not cls_i._have_objections():
                print("Done -- no objections")
                break
            else:
                print("Still running: last_pending=%d pending=%d" % (
                    last_pending_time_reqs, self.pending_time_reqs))
                if last_pending_time_reqs == self.pending_time_reqs:
                    self.ep.update_comm_mode(comm_mode_e.Automatic, comm_state_e.Released)
                    while self.pending_time_reqs == last_pending_time_reqs:
                        print("--> process_one_message")
                        if self.ep.process_one_message() == -1:
                            raise Exception("Unexpected disconnect")
                            break
                        print("<-- process_one_message")
                # Tell the simulator to go run
            last_pending_time_reqs = self.pending_time_reqs
        
        pass
    
    def update_state(self):
        pass
    
    def event(self, ev):
        kind = ev.kind()
        print("event: %s" % str(kind))
        
        if kind == EventTypeE.OutInvokeReqB:
            self.pending_time_reqs += 1
        if kind == EventTypeE.InInvokeRspB:
            self.pending_time_reqs -= 1
        pass
    
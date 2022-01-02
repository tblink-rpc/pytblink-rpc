'''
Created on Dec 27, 2021

@author: mballance
'''
import asyncio
from enum import Enum, auto
import importlib
import traceback

from tblink_rpc.impl.iftype_rgy import IftypeRgy
from tblink_rpc.rt.runner import Runner
from tblink_rpc_core.endpoint import comm_mode_e, comm_state_e
from tblink_rpc_core.endpoint_listener import EndpointListener
from tblink_rpc_core.event_type_e import EventTypeE


class State(Enum):
    AwaitInit = auto()
    AwaitBuilt = auto()
    RunPropagate = auto()
    ProcessMessages = auto()

class EndpointSequencer(object):
    
    def __init__(self, ep, backend, is_async):
        self.ep = ep
        self.backend = backend
        self.ep.addListener(self.event)
        self.is_async = is_async
        self.runner = None
        self.new_time_req = False
        self.pending_time_reqs = 0
        self.outstanding_nb_reqs = 0
        self.inbound_events = 0
        self.terminated = False
        self.cls_i = None
        self.async_state = State.AwaitInit

    def run(self):
        if self.is_async:
            self._async_run()
        else:
            self._sync_run()
            
    def _sync_run(self):
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
        
        self._create_tb()
        
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
            self.cls_i._do_connect(self.ep)
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
            self.cls_i._do_start()
        except Exception as e:
            print("Exception during start: %s" % str(e), flush=True)
            traceback.print_exc()
            raise e

        while not self.terminated:
            # Spin the loop while we have outstanding non-blocking calls
            # or while we're still receiving outbound time-centric requests
            print("--> Process Python activity", flush=True)
            while True:
                self.new_time_req = False

                self.propagate_events()                

                # print(" -- outstanding_nb_reqs=%d new_time_req=%d" % (
                #     self.outstanding_nb_reqs, self.new_time_req), flush=True)
                # if self.outstanding_nb_reqs == 0 and not self.new_time_req:
                #     print("  -- No new events", flush=True)
                #     break
                # elif self.outstanding_nb_reqs > 0:
                #     if self.ep.process_one_message() == -1:
                #         self.terminated = True
                #         raise Exception("Unexpected disconnect")
            print("<-- Process Python activity", flush=True)
            
            if not self.cls_i._have_objections():
                print("Done -- no objections", flush=True)
                break
            else:
                print("--> Release peer", flush=True)
                self.ep.update_comm_mode(comm_mode_e.Automatic, comm_state_e.Released)
                print("<-- Release peer", flush=True)
                
                print("--> Await events", flush=True)
                self.inbound_events = 0
                while self.inbound_events == 0:
                    print("--> process_one_message", flush=True)
                    if self.ep.process_one_message() == -1:
                        raise Exception("Unexpected disconnect")
                    print("<-- process_one_message", flush=True)
                print("<-- Await events: %d" % self.inbound_events, flush=True)
        
        pass        
        
    def _create_tb(self):
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
            self.cls_i = cls("root", None)
        except Exception as e:
            print("Execption: %s" % str(e), flush=True)
            raise e

        # Register all discovered types with the endpoint
        IftypeRgy.inst().endpoint_added(self.ep)
            
        # Run the build phase
        try:
            self.cls_i._do_build(self.backend, self.ep)
        except Exception as e:
            print("Exception during build: %s" % str(e))
            raise e
        
        if self.ep.build_complete() == -1:
            raise Exception("TbLink Error: build_complete failed")
    
    def propagate_events(self):
        loop = asyncio.get_event_loop()
        def _end_reschedule():
            nonlocal loop
            print("-- _end_reschedule")
            loop.stop()        
            
        loop.call_soon(_end_reschedule)
        loop.run_forever()
       
        print(" -- outstanding_nb_reqs=%d new_time_req=%d" % (
            self.outstanding_nb_reqs, self.new_time_req), flush=True)
        if self.outstanding_nb_reqs == 0 and not self.new_time_req:
            print("  -- No new events", flush=True)
            return True
        elif self.outstanding_nb_reqs > 0:
            if self.ep.process_one_message() == -1:
                self.terminated = True
                raise Exception("Unexpected disconnect")        
        return False
    
    def _async_run(self):
        """"""
        print("--> _async_run", flush=True)
        if self.async_state == State.AwaitInit:
            if self.ep.is_init() == 1:
                # Creates the TB class and calls build_complete
                self._create_tb()
                self.async_state = State.AwaitBuilt
                
        if self.async_state == State.AwaitBuilt:
            code = self.ep.is_build_complete()
            if code == -1:
                raise Exception("TbLink Error: is_build_complete failed")
            elif code == 1:
                
                try:
                    self.cls_i._do_connect(self.ep)
                except Exception as e:
                    print("Exception during connect: %s" % str(e), flush=True)
                    traceback.print_exc()
                    raise e
                    
                if self.ep.connect_complete() == -1:
                    raise Exception("TbLink Error: connect_complete failed")
                self.async_state = State.AwaitConnected
                
        if self.async_state == State.AwaitConnected:
            code = self.ep.is_connect_complete()
            
            if code == -1:
                raise Exception("TbLink Error: is_connect_complete failed")
            elif code == 1:
                try:
                    self.cls_i._do_start()
                except Exception as e:
                    print("Exception during start: %s" % str(e), flush=True)
                    traceback.print_exc()
                    raise e
                
                self.async_state = State.RunPropagate
                
        if self.async_state == State.RunPropagate:
            loop = asyncio.get_event_loop()
            
            def _end_reschedule():
                nonlocal loop
                print("-- _end_reschedule")
                loop.stop()        
            
            loop.call_soon(_end_reschedule)
            loop.run_forever()            
            
            if not self.cls_i._have_objections():
                print("No objections... Time to halt")
            else:
                print("Release peer")
                self.ep.update_comm_mode(comm_mode_e.Automatic, comm_state_e.Released)
                        
        print("<-- _async_run", flush=True)
        pass
    
    def event(self, ev):
        kind = ev.kind()
        print("event: %s" % str(kind), flush=True)
        
        if kind == EventTypeE.OutInvokeReqB:
            self.pending_time_reqs += 1
            self.new_time_req = True
        elif kind == EventTypeE.InInvokeRspB:
            self.pending_time_reqs -= 1
        elif kind == EventTypeE.OutInvokeReqNB:
            self.outstanding_nb_reqs += 1
        elif kind == EventTypeE.InInvokeRspNB:
            self.outstanding_nb_reqs -= 1
        elif kind == EventTypeE.InInvokeReqB:
            self.inbound_events += 1
        elif kind == EventTypeE.InInvokeReqNB:
            self.inbound_events += 1
            
        if self.is_async:
            self._async_run()
        pass
    
'''
Created on Dec 27, 2021

@author: mballance
'''
from tblink_rpc_core.endpoint_listener import EndpointListener
import importlib
from tblink_rpc.rt.runner import Runner
import asyncio

class EndpointSequencer(object):
    
    def __init__(self, ep, is_async):
        self.ep = ep
        self.ep.addListener(self.event)
        self.is_async = is_async
        self.runner = None

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
            
        # Run the build phase
        try:
            cls_i._do_build(self.ep)
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
            print("Exception during connect: %s" % str(e), flush=True)
            raise e

        ev = asyncio.Event()        
        loop = asyncio.get_event_loop()
        def _end_reschedule():
            nonlocal ev
            ev.set()
            
        while True:
            loop.call_soon(_end_reschedule)
            if not ev.is_set():
                loop.run_until_complete(ev.wait())
            ev.clear()
            
            if not cls_i._have_objections():
                print("Done -- no objections")
                break
            else:
                print("Still running")
                # Tell the simulator to go run
        
        pass
    
    def update_state(self):
        pass
    
    def event(self, ev):
        print("event")
        pass
    
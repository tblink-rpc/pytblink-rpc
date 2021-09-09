'''
Created on Aug 25, 2021

@author: mballance
'''
import asyncio

from tblink.model.component import Component


class Runner(object):
    """
    Runs build/connect/start/run on the specified class or object.
    Assumes an endpoint has already been established
    """
    
    
    def __init__(self, 
                 T_or_inst,
                 endpoint):
        self.T_or_inst = T_or_inst
        self.inst = None
        self.endpoint = endpoint
        
    async def run(self):
        print("--> run", flush=True)
        
        print("type: %s" % str(type(self.T_or_inst)))
        
        if isinstance(self.T_or_inst, Component):
            # Need to create an instance
            self.inst = self.T_or_inst
        else:
            self.inst = self.T_or_inst(None)
            
        # Run the build phase first
        self.inst._do_build(self.endpoint)
        
        # Now, collect what has been registered by
        # the build phase
        await self.endpoint.build_complete()
        
        # TODO: notify of a successful build phase
        
        # Now, run connect for the user
        self.inst._do_connect()
        
        # TODO: notify of a successful connect phase
        await self.endpoint.connect_complete()
        
        # Finally, invoke the start methods
        self.inst._do_start()

        ev = asyncio.Event()        
        loop = asyncio.get_event_loop()
        def _end_reschedule():
            nonlocal ev
            print("_end_reschedule")
            ev.set()

        while True:
            print("--> Schedule loop")
            loop.call_soon(_end_reschedule)
            print("--> ev.wait")
            await ev.wait()
            print("<-- ev.wait")
            ev.clear()
            
            if not self.inst._have_objections():
                print("Done")
                break
            
            print("<-- Schedule loop")
                
            

        # TODO: Run loop
        
        
        print("<-- run", flush=True)

        pass
    

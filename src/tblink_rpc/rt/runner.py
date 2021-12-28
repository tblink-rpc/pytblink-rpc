'''
Created on Aug 25, 2021

@author: mballance
'''
import asyncio

from tblink_rpc.component import Component


class Runner(object):
    """
    Runs build/connect/start/run on the specified class or object.
    Assumes an endpoint has already been established
    """

    DEBUG_EN = False
    
    def __init__(self, 
                 T_or_inst,
                 endpoint):
        self.T_or_inst = T_or_inst
        self.inst = None
        self.endpoint = endpoint
        
    async def run(self):
        if Runner.DEBUG_EN:
            print("--> run", flush=True)
        
        if Runner.DEBUG_EN:
            print("type: %s" % str(type(self.T_or_inst)))
            
        # Ensure the initialization sequence is complete
        while not self.endpoint.is_init():
            await self.endpoint.process_one_message_a()
        
        if isinstance(self.T_or_inst, Component):
            # Need to create an instance
            self.inst = self.T_or_inst
        else:
            self.inst = self.T_or_inst(None)
            
        # Run the build phase first
        self.inst._do_build(self.endpoint)
        
        # Now, collect what has been registered by
        # the build phase
        self.endpoint.build_complete()
        
        while not self.endpoint.is_build_complete():
            await self.endpoint.process_one_message_a()
        
        # TODO: notify of a successful build phase
        
        # Now, run connect for the user
        self.inst._do_connect()
        
        # TODO: notify of a successful connect phase
        self.endpoint.connect_complete()
        
        while not self.endpoint.is_connect_complete():
            await self.endpoint.process_one_message_a()
        
        # Finally, invoke the start methods
        self.inst._do_start()

        ev = asyncio.Event()        
        loop = asyncio.get_event_loop()
        def _end_reschedule():
            nonlocal ev
            if Runner.DEBUG_EN:
                print("_end_reschedule")
            ev.set()

        while True:
            if Runner.DEBUG_EN:
                print("--> Schedule loop")
            loop.call_soon(_end_reschedule)
            if Runner.DEBUG_EN:
                print("--> ev.wait")
            if not ev.is_set():
                await ev.wait()
            if Runner.DEBUG_EN:
                print("<-- ev.wait")
            ev.clear()

            if Runner.DEBUG_EN:
                print("Objections: %d" % self.inst.objections)
            if not self.inst._have_objections():
                if Runner.DEBUG_EN:
                    print("Done")
                break
            
            if Runner.DEBUG_EN:
                print("<-- Schedule loop")
                
            

        # TODO: Run loop
        
        
        if Runner.DEBUG_EN:
            print("<-- run", flush=True)

        pass
    

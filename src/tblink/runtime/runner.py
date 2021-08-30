'''
Created on Aug 25, 2021

@author: mballance
'''
from tblink.component import Component

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

        # TODO: Run loop
        
        print("<-- run", flush=True)

        pass
    

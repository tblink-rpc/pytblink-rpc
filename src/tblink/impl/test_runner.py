'''
Created on Jul 11, 2021

@author: mballance
'''

class TestRunner(object):
    
    def __init__(self, endpoint, test_class):
        self.endpoint = endpoint
        self.test_class = test_class
        pass
    
    async def run(self):
        # Let's first ensure that we can load the
        # desired class
        
        # First, let's get the arguments
        init_resp = await self.endpoint.init()
        
        pass
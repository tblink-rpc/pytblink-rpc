'''
Created on Jul 11, 2021

@author: mballance
'''

class EndpointRgy():
    
    _inst = None
    
    def __init__(self):
        self._endpoints = []
        pass
    
    def endpoints(self):
        return self._endpoints
    
    def add_endpoint(self, ep):
        self._endpoints.append(ep)
    
    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = EndpointRgy()
        return cls._inst
    
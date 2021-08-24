'''
Created on Aug 13, 2021

@author: mballance
'''

class IEndpoint(object):
    
    def __init__(self):
        pass
    
    async def build_complete(self):
        pass
    
    async def connect_complete(self):
        pass
    
    async def shutdown(self):
        pass
    
    async def run_until_event(self):
        pass
    
    
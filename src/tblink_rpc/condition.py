'''
Created on Dec 27, 2021

@author: mballance
'''
from tblink_rpc.lock import Lock

class Condition(Lock):

    def notify(self):
        pass
    
    def notify_all(self):
        pass
    
    async def wait(self):
        pass
    
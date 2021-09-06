'''
Created on Sep 4, 2021

@author: mballance
'''
from tblink.impl.backend import Backend
import asyncio

class BackendAsyncio(Backend):
    
    def event(self):
        return asyncio.Event()
    
    def fork(self, coro):
        return asyncio.ensure_future(coro)
    
    def lock(self):
        return asyncio.Lock()
    
    def semaphore(self):
        return asyncio.Semaphore()
    
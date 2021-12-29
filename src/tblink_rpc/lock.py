'''
Created on Dec 27, 2021

@author: mballance
'''

class Lock(object):
    
    async def __aenter__(self):
        raise NotImplementedError("__aenter__ not implemented by %s" % str(type(self)))
    
    async def __aexit__(self, t, v, tb):
        raise NotImplementedError("__aexit__ not implemented by %s" % str(type(self)))
    
    async def acquire(self):
        raise NotImplementedError("acquire not implemented by %s" % str(type(self)))
    
    def release(self):
        raise NotImplementedError("release not implemented by %s" % str(type(self)))
        
    
    
    
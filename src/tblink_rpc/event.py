'''
Created on Dec 27, 2021

@author: mballance
'''

class Event(object):
    
    async def wait(self):
        raise NotImplementedError("wait not implemented by %s" % str(type(self)))
    
    def set(self):
        raise NotImplementedError("set not implemented by %s" % str(type(self)))
    
    def clear(self):
        raise NotImplementedError("clear not implemented by %s" % str(type(self)))
    
    def is_set(self):
        raise NotImplementedError("is_set not implemented by %s" % str(type(self)))
    
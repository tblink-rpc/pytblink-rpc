'''
Created on Sep 4, 2021

@author: mballance
'''

class Backend(object):
    
    def event(self):
        raise NotImplementedError("Backend.event not implemented for class %s" % str(type(self)))
    
    def fork(self, coro):
        raise NotImplementedError("Backend.fork not implemented for class %s" % str(type(self)))
    
    def lock(self):
        raise NotImplementedError("Backend.lock not implemented for class %s" % str(type(self)))

    def semaphore(self):
        raise NotImplementedError("Backend.semaphore not implemented for class %s" % str(type(self)))
    
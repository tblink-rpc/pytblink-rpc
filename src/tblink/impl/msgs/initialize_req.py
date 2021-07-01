'''
Created on Apr 2, 2021

@author: mballance
'''

class InitializeReq(object):
    
    def __init__(self):
        self.module = None
        self.entry = None
    
    def dump(self):
        pass
    
    @staticmethod
    def load(msg) -> 'InitializeReq':
        ret = InitializeReq()
        
        if "module" in msg.keys():
            ret.module = msg["module"]
            
        if "entry" in msg.keys():
            ret.entry = msg["entry"]
        
        return ret
    
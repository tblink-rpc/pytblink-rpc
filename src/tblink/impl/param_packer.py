'''
Created on Sep 5, 2021

@author: mballance
'''
from tblink_rpc_core.param_val_vec import ParamValVec

class ParamPacker(object):
    
    def __init__(self, ep, method_t):
        self.ep = ep
        self.method_t = method_t
        
    def pack(self, *args, **kwargs) -> ParamValVec:
        pass
'''
Created on Dec 28, 2021

@author: mballance
'''
from tblink_rpc.backend import Backend

class BackendEP(Backend):
    
    def __init__(self, ep):
        self._ep = ep
    
    pass
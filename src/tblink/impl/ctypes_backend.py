'''
Created on Mar 8, 2021

@author: mballance
'''
from tblink.backend import Backend

class CTypesBackend(Backend):
    
    def __init__(self, api_ptr):
        print("CtypesBackend::init " + hex(api_ptr))
        pass
    
    def simtime(self)->int:
        pass
    
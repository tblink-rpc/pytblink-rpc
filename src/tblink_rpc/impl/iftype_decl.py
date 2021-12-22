'''
Created on Aug 24, 2021

@author: mballance
'''
from typing import List
from tblink_rpc.impl.methodtype_decl import MethodTypeDecl

class IftypeDecl(object):
    """Captures the interface type from the user facade"""
    
    def __init__(self, name, T, methods : List[MethodTypeDecl]):
        self.name = name
        self.T = T
        self.methods = methods
        self.method_m = {}
        for m in methods:
            self.method_m[m.name] = m
        self.method_t2method_m = {}

        # Must be able to attach parameters to the interface type
        self.params = []
            
    def find_method(self, name):
        if name in self.method_m.keys():
            return self.method_m[name]
        else:
            return None
        
    
    
    
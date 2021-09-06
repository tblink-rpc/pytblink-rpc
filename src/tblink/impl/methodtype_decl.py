'''
Created on Aug 24, 2021

@author: mballance
'''
from typing import List, Tuple
from tblink.impl.type_decl import TypeDecl

class MethodTypeDecl(object):
    """Method-Type representation used by the Python user facade"""
    
    def __init__(self, 
                 name, 
                 id,
                 rtype,
                 params,
                 is_task, 
                 is_export):
        self.name = name
        self.id = id
        self.rtype = rtype
        self.params : List[Tuple[str,TypeDecl]] = params
        self.is_task = is_task
        self.is_export = is_export
        self.method_t_ep_m = {}
        
    
    
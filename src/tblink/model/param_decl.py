'''
Created on Aug 24, 2021

@author: mballance
'''
from tblink.model.type_decl import TypeDecl

class ParamDecl(object):
    
    def __init__(self, ptype : TypeDecl, pname : str):
        self.ptype = ptype
        self.pname = pname
        
        
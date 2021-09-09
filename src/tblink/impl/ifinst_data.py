'''
Created on Sep 7, 2021

@author: mballance
'''
from tblink.impl.iftype_decl import IftypeDecl
from tblink_rpc_core.interface_inst import InterfaceInst

class IfInstData(object):
    
    def __init__(self, 
                 ep, 
                 iftype : IftypeDecl,
                 ifinst : InterfaceInst, 
                 is_mirror):
        self.ep = ep
        self.iftype = iftype
        self.ifinst = ifinst
        self.is_mirror = is_mirror
        self.methodt2decl_m = {}


'''
Created on Sep 7, 2021

@author: mballance
'''
from tblink_rpc.impl.iftype_decl import IftypeDecl
from tblink_rpc_core.interface_inst import InterfaceInst
from tblink_rpc.backend import Backend

class IfInstData(object):
    
    def __init__(self, 
                 backend : Backend,
                 iftype : IftypeDecl,
                 ifinst : InterfaceInst, 
                 is_mirror):
        self.backend = backend
        self.iftype = iftype
        self.ifinst = ifinst
        self.inst_name = ifinst.name()
        self.is_mirror = is_mirror
        self.methodt2decl_m = {}


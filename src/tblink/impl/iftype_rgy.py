'''
Created on Aug 22, 2021

@author: mballance
'''
from tblink_rpc_core.endpoint_mgr import EndpointMgr
from tblink_rpc_core.endpoint_mgr_listener import EndpointMgrListener
from tblink.impl.iftype_decl import IftypeDecl
from tblink.impl.param_type_builder import ParamTypeBuilder

class IftypeRgy(EndpointMgrListener):
    
    _inst = None
    
    def __init__(self):
        self.iftypes = []
        self.iftype_name_m = {}
        self.iftype_type_m = {}
        pass
    
    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = IftypeRgy()
            
            # Add ourselves as an endpoint listener. 
            # We'll use the 'endpoint_added' callback to register types
            EndpointMgr.inst().add_listener(cls._inst)
            
        return cls._inst
    
    def endpoint_added(self, ep):
        for iftype in self.iftypes:
            self._define_iftype(ep, iftype)
            
    def add_iftype(self, iftype):
        if iftype.name in self.iftype_name_m.keys():
            raise Exception("Duplicate iftype %s" % iftype.name)
        self.iftypes.append(iftype)
        self.iftype_name_m[iftype.name] = iftype
        self.iftype_type_m[iftype.T] = iftype
        
        # Add to known endpoints
        for ep in EndpointMgr.inst().endpoints:
            self._define_iftype(ep, iftype)
        
    
    def find_by_name(self, name):
        if name in self.iftype_m.keys():
            return self.iftype_m[name]
        else:
            return None
        
    def find_by_type(self, T) -> IftypeDecl:
        if T in self.iftype_type_m.keys():
            return self.iftype_type_m[T]
        else:
            return None
        
    def _define_iftype(self, ep, iftype : IftypeDecl):
        iftype_b = ep.newInterfaceTypeBuilder(iftype.name)
        ptb = ParamTypeBuilder(iftype_b)
        
        for i,m in enumerate(iftype.methods):
            mtb = iftype_b.newMethodTypeBuilder(
                m.name,
                i,
                ptb.build(m.rtype),
                m.is_export,
                m.is_task)
            
            for name,ptype in m.params:
                mtb.add_param(
                    name,
                    ptb.build(ptype))
                
            mt = iftype_b.add_method(mtb)
            m.method_t_ep_m[ep] = mt
            iftype.method_t2method_m[mt] = m
        
        ep.defineInterfaceType(iftype_b)
        

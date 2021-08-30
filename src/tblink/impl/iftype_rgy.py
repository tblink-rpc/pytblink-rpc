'''
Created on Aug 22, 2021

@author: mballance
'''
from tblink_rpc_core.endpoint_mgr import EndpointMgr
from tblink_rpc_core.endpoint_mgr_listener import EndpointMgrListener

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
        
    def find_by_type(self, T):
        if T in self.iftype_type_m.keys():
            return self.iftype_type_m[T]
        else:
            return None
        
    def _define_iftype(self, ep, iftype):
        iftype_b = ep.newInterfaceTypeBuilder(iftype.name)
        
        # TODO: define methods
        
        ep.defineInterfaceType(iftype_b)
        

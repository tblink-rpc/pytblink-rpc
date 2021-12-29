'''
Created on Aug 22, 2021

@author: mballance
'''
from tblink_rpc_core.endpoint_mgr import EndpointMgr
from tblink_rpc_core.endpoint_mgr_listener import EndpointMgrListener
from tblink_rpc.impl.iftype_decl import IftypeDecl
from tblink_rpc.impl.param_type_builder import ParamTypeBuilder
from typing import List

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
        print("endpoint_added: %d iftypes" % len(self.iftypes))
        for iftype in self.iftypes:
            self._define_iftype(ep, iftype)
        for iftype in ep.getInterfaceTypes():
            print("iftype: %s" % iftype.name())
            
    def build_bfms(self, ep) -> List[object]:
        ret = []
        print("build_bfms", flush=True)
        for ifinst in ep.getPeerInterfaceInsts():
            print("ifinst: %s" % ifinst.name(), flush=True)
            tname = ifinst.type().name()
            
            if tname not in self.iftype_name_m.keys():
                raise Exception("Interface type %s (instance %s) is not registered" % (
                    tname, ifinst.name()))

            try:            
                _iftype : IftypeDecl = self.iftype_name_m[tname]
                print("iftype: %s %s" % (str(type(_iftype)), str(_iftype)))
            
                bfm_inst = _iftype.T.mkMirrorInst(ep, ifinst.name())
                ret.append(bfm_inst)
                print("  ifinst: %s %s" % (ifinst.name(), ifinst.type().name()))
            except Exception as e:
                print("Exception: %s" % str(e), flush=True)
        return ret

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
        print("_define_iftype: Adding interface-type %s" % iftype.name)
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
            iftype.method_t2method_m[mt.name()] = m
        
        ep.defineInterfaceType(iftype_b)
        

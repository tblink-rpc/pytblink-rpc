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
    def reset(cls):
        cls._inst = None
        return cls.inst()
    
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
            
    def define_iftypes(self, ep):
        print("define_ifrypes: %d iftypes" % len(self.iftypes))
        for iftype in self.iftypes:
            self._define_iftype(ep, iftype)
            
    def build_bfms(self, backend) -> List[object]:
        ret = []
        print("build_bfms", flush=True)
        for ifinst in backend.ep().getPeerInterfaceInsts():
            print("ifinst: %s (%s)" % (ifinst.name(), str(ifinst.type())), flush=True)
            tname = ifinst.type().name()
            
            if tname not in self.iftype_name_m.keys():
                raise Exception("Interface type %s (instance %s) is not registered" % (
                    tname, ifinst.name()))

            try:            
                _iftype : IftypeDecl = self.iftype_name_m[tname]
                print("iftype: %s %s" % (str(type(_iftype)), str(_iftype)))
            
                bfm_inst = _iftype.T.mkMirrorInst(backend, ifinst.name())
                ret.append(bfm_inst)
                print("  ifinst: %s %s" % (ifinst.name(), ifinst.type().name()))
            except Exception as e:
                print("Exception: %s" % str(e), flush=True)
                raise e
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
        
        if ep.findInterfaceType(iftype.name) is not None:
            return
        
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

        # TODO: add in create proxy        
        ep.defineInterfaceType(
            iftype_b, 
            lambda : iftype.T.mkInst(ep, "").invoke_f, 
            lambda : iftype.T.mkMirrorInst(ep, "").invoke_f)

        

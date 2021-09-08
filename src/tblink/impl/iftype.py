'''
Created on Sep 7, 2021

@author: mballance
'''
from tblink.impl.ctor import Ctor
from tblink.impl.ifinst_data import IfInstData
from tblink.impl.iftype_decl import IftypeDecl
from tblink.impl.iftype_rgy import IftypeRgy
from tblink_rpc_core.endpoint_mgr import EndpointMgr
import tblink

class iftype():
    """Implementation for the 'tblink.iftype' decorator"""
    
    def __init__(self, kwargs):
        self.name = None
        self.public = True
        
        for key in kwargs.keys():
            if key == "name":
                self.name = kwargs[key]
            elif key == "public":
                self.public = bool(kwargs[key])
            else:
                raise Exception("Unsupport iftype kwarg %s" % key)
            
    @staticmethod
    async def _invoke_b(self, f, params):
        ifinst_data = self._ifinst_data
        print("_invoke_b")
        # TODO: call actual method
        
        # TODO: send response back via endpoint
        print("Send response via %s" % str(ifinst_data.ep))
            
    @staticmethod
    def _invoke_req_f(self, ifinst, method_t, call_id, params):
        ifinst_data = self._ifinst_data
        
        # TODO: lookup method_decl class so we know what to call
        
        # TODO: Convert parameters to native form
        call_params = []
        
        if method_t.is_blocking:
            print("is_blocking")
            tblink.fork(iftype._invoke_b(self, None, call_params))
        else:
            print("non_blocking")
            
        # TODO: need to map method_t -> closure
        print("req_f")

    @staticmethod
    def _mkInst(T, _ep, _inst_name, *args, **kwargs):
        if _ep is None:
            _ep = EndpointMgr.inst().default()
            
        ret = T.__new__(T)
        
        # iftype, here, is the Python proxy. We need to
        # get the actual endpoint-specific 'iftype' from the
        # endpoint
        iftype_p : IftypeDecl = IftypeRgy.inst().find_by_type(T)
        iftype = _ep.findInterfaceType(iftype_p.name)

        ifinst = _ep.defineInterfaceInst(
            iftype, 
            _inst_name, 
            False, 
            ret.invoke_f)

        ret._ifinst_data = IfInstData(_ep, ifinst, False)

        T.__init__(ret, *args, *kwargs)

        print("ep: %s" % str(_ep))

        return ret
    
    @staticmethod
    def _mkMirrorInst(T, _ep, _inst_name, *args, **kwargs):
        if _ep is None:
            _ep = EndpointMgr.inst().default()
            
        ret = T.__new__(T)
        
        iftype_p = IftypeRgy.inst().find_by_type(T)
        iftype = _ep.findInterfaceType(iftype_p.name)

        ifinst = _ep.defineInterfaceInst(
            iftype, 
            _inst_name, 
            True, 
            ret.invoke_f)

        ret._ifinst_data = IfInstData(_ep, ifinst, True)

        T.__init__(ret, *args, *kwargs)
        
        print("ep: %s" % str(_ep))
        
        return ret
    
    @staticmethod
    def _inst_name(self): 
        if not hasattr(self, "_ifinst_data"):
            raise Exception("Class %s (%s) was not created with 'mk' or 'mk_mirror'" % (
                str(self), str(type(self))))
        return self._ifinst_data.inst_name
        
    @staticmethod
    def _is_mirror(self): 
        if not hasattr(self, "_ifinst_data"):
            raise Exception("Class %s (%s) was not created with 'mk' or 'mk_mirror'" % (
                str(self), str(type(self))))
        return self._ifinst_data.is_mirror    
            
    def __call__(self, T):
        
        if self.name is None:
            self.name = T.__name__

        T.invoke_f = iftype._invoke_req_f
        T.mkInst = lambda _ep, _inst_name, *args, **kwargs: iftype._mkInst(T, _ep, _inst_name, *args, *kwargs)
        T.mkMirrorInst = lambda _ep, _inst_name, *args, **kwargs: iftype._mkMirrorInst(T, _ep, _inst_name, *args, *kwargs)
        T.inst_name = iftype._inst_name
        T.is_mirror = iftype._is_mirror

        # TODO: do we need to hook the ctor?
        Ctor.inst().add_iftype(
            T,
            self.name)
#            self.public)
        return T

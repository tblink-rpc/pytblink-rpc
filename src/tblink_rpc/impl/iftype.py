'''
Created on Sep 7, 2021

@author: mballance
'''
import tblink_rpc
from tblink_rpc.impl.ctor import Ctor
from tblink_rpc.impl.ifinst_data import IfInstData
from tblink_rpc.impl.iftype_decl import IftypeDecl
from tblink_rpc.impl.iftype_rgy import IftypeRgy
from tblink_rpc_core.endpoint_mgr import EndpointMgr
from tblink_rpc.impl.param_unpacker import ParamUnpacker
from tblink_rpc.impl import ifinst_data
from tblink_rpc_core.method_type import MethodType
from tblink_rpc.impl.packer import Packer

class iftype():
    """Implementation for the 'tblink.iftype' decorator"""
    
    def __init__(self, args, kwargs):
        self.name = None
        self.public = True
        
        print("args=%s" % str(args))
        print("kwargs=%s" % str(kwargs))
        
        for key in kwargs.keys():
            if key == "name":
                self.name = kwargs[key]
            elif key == "public":
                self.public = bool(kwargs[key])
            else:
                raise Exception("Unsupport iftype kwarg %s" % key)

        if len(args) == 1:            
            if self.name is None:
                self.name = args[0]
            else:
                raise Exception("Name specified in two ways")
        else:
            raise Exception("Only zero or one argument permitted")
            
    @staticmethod
    async def _invoke_b(self, ifinst, call_id, method_t : MethodType, params):
        ifinst_data = self._ifinst_data
        method_d = ifinst_data.iftype.method_t2method_m[method_t.name()]
        
        # Call actual method
        ret = await method_d.T(self, *params)
        
        if method_t.rtype() is not None:
            retval = Packer(ifinst_data.backend.ep()).pack_value(ret, method_t.rtype())
        else:
            retval = None

        ifinst.invoke_rsp(call_id, retval)

    @staticmethod
    def _invoke_req_f(self, ifinst, method_t, call_id, params):
        print("--> _invoke_req_f %s" % str(type(method_t)), flush=True)
        # Note: 'self' in this context is the user's interface-impl class
        ifinst_data : IfInstData = self._ifinst_data
        
        
        # Convert parameters to native form
        call_params = ParamUnpacker().unpack(method_t, params)

        ret = None        
        if method_t.is_blocking():
            print("-- is_blocking", flush=True)
            ifinst_data.backend.start_soon(iftype._invoke_b(
                self, 
                ifinst,
                call_id, 
                method_t,
                call_params))
        else:
            print("-- non_blocking", flush=True)
            method_d = ifinst_data.iftype.method_t2method_m[method_t.name()]
            ret = method_d.T(self, *call_params)
            
            if method_t.rtype() is not None:
                retval = Packer(ifinst_data.backend.ep()).pack_value(ret, method_t.rtype())
            else:
                retval = None

            ifinst.invoke_rsp(call_id, retval)
            
        print("<-- _invoke_req_f ", flush=True)
            
        return ret

    @staticmethod
    def _mkInst(T, _backend, _inst_name, *args, **kwargs):
        if _backend is None:
            raise Exception("No backend specified")
            _ep = EndpointMgr.inst().default()
            
        ret = T.__new__(T)
        
        # iftype, here, is the Python proxy. We need to
        # get the actual endpoint-specific 'iftype' from the
        # endpoint
        iftype_p : IftypeDecl = IftypeRgy.inst().find_by_type(T)
        _iftype = _backend.ep().findInterfaceType(iftype_p.name)
        
        if _iftype is None:
            raise Exception("iftype %s is not registered with endpoint" % iftype_p.name)

        ifinst = _backend.ep().defineInterfaceInst(
            _iftype, 
            _inst_name, 
            False, 
            ret.invoke_f)

        ret._ifinst_data = IfInstData(_backend, iftype_p, ifinst, False)

        T.__init__(ret, *args, *kwargs)

        return ret
    
    @staticmethod
    def _mkMirrorInst(T, _backend, _inst_name, *args, **kwargs):
        print("_mkMirrorInst: %s" % _inst_name)
        if _backend is None:
            raise Exception("No backend specified")
            _backend = EndpointMgr.inst().default()
            
        ret = T.__new__(T)
        
        iftype_p = IftypeRgy.inst().find_by_type(T)
        _iftype = _backend.ep().findInterfaceType(iftype_p.name)
        
        if _iftype is None:
            raise Exception("iftype %s is not registered with endpoint" % iftype_p.name)

        ifinst = _backend.ep().defineInterfaceInst(
            _iftype, 
            _inst_name, 
            True, 
            ret.invoke_f)
        
        print("ifinst=%s (%s)" % (str(ifinst), str(type(ifinst))))

        ret._ifinst_data = IfInstData(_backend, iftype_p, ifinst, True)

        T.__init__(ret, *args, *kwargs)
        
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

        setattr(T, "invoke_f", iftype._invoke_req_f)
        T.mkInst = lambda _backend, _inst_name, *args, **kwargs: iftype._mkInst(T, _backend, _inst_name, *args, *kwargs)
        T.mkMirrorInst = lambda _backend, _inst_name, *args, **kwargs: iftype._mkMirrorInst(T, _backend, _inst_name, *args, *kwargs)
        
        setattr(T, "inst_name", iftype._inst_name)
        T.is_mirror = iftype._is_mirror

        # TODO: do we need to hook the ctor?
        Ctor.inst().add_iftype(
            T,
            self.name)
#            self.public)
        return T

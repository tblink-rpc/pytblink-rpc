'''
Created on Jul 8, 2020

@author: ballance
'''

import ctypes
from typing import Generic, TypeVar, List
import typing

from .impl.test_rgy import TestRgy
from tblink.impl.ctor import Ctor
from tblink_rpc_core.endpoint_mgr import EndpointMgr
from tblink.impl.iftype_rgy import IftypeRgy
from tblink.impl.param_packer import ParamPacker
import tblink

class IfInstData(object):
    
    def __init__(self, ep, ifinst, is_mirror):
        self.ep = ep
        self.ifinst = ifinst
        self.is_mirror = is_mirror

class _iftype():
    
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
            
    def __call__(self, T):
        
        def _mkInst(_ep, _inst_name, *args, **kwargs):
            if _ep is None:
                _ep = EndpointMgr.inst().default()
                
            ret = T.__new__(T)
            
            # iftype, here, is the Python proxy. We need to
            # get the actual endpoint-specific 'iftype' from the
            # endpoint
            iftype_p = IftypeRgy.inst().find_by_type(T)
            iftype = _ep.findInterfaceType(iftype_p.name)

            ifinst = _ep.defineInterfaceInst(iftype, _inst_name, False, None)

            ret._ifinst_data = IfInstData(_ep, ifinst, False)

            T.__init__(ret, *args, *kwargs)

            print("ep: %s" % str(_ep))

            return ret
        
        def _mkMirrorInst(_ep, _inst_name, *args, **kwargs):
            if _ep is None:
                _ep = EndpointMgr.inst().default()
                
            ret = T.__new__(T)
            
            iftype_p = IftypeRgy.inst().find_by_type(T)
            iftype = _ep.findInterfaceType(iftype_p.name)

            ifinst = _ep.defineInterfaceInst(iftype, _inst_name, True, None)

            ret._ifinst_data = IfInstData(_ep, ifinst, True)

            T.__init__(ret, *args, *kwargs)
            
            print("ep: %s" % str(_ep))
            
            return ret
        
        def _inst_name(self): 
            if not hasattr(self, "_ifinst_data"):
                raise Exception("Class %s (%s) was not created with 'mk' or 'mk_mirror'" % (
                    str(self), str(type(self))))
            return self._ifinst_data.inst_name
        
        def _is_mirror(self): 
            if not hasattr(self, "_ifinst_data"):
                raise Exception("Class %s (%s) was not created with 'mk' or 'mk_mirror'" % (
                    str(self), str(type(self))))
            return self._ifinst_data.is_mirror
        
        if self.name is None:
            self.name = T.__name__
            
        T.mkInst = _mkInst
        T.mkMirrorInst = _mkMirrorInst
        T.inst_name = _inst_name
        T.is_mirror = _is_mirror

        # TODO: do we need to hook the ctor?
        Ctor.inst().add_iftype(
            T,
            self.name)
#            self.public)
        return T


def iftype(*args, **kwargs):
    """Marks an interface type"""
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        # No-argument form
        return _iftype({})(args[0])
    else:
        return _iftype(kwargs)
    
class _impfunc(object):
      
    def __init__(self, kwargs):
        pass
      
    def __call__(self, T):
        # Must capture the function for use in the
        # mirror case.
        def _impfunc_impl(self, *args, **kwargs):
            if_data = self._ifinst_data
            print("_impfunc_impl: is_mirror=%s" % (str(if_data.is_mirror)))
            
            if if_data.is_mirror:
                # This is actually an export, since the ifinst is a mirror
                # It should be okay to invoke it directly.
                T(self, *args, **kwargs)                 
            else:
                # This is a true import, so we need to queue the
                # call and send it to the other side
                print("TODO: queue method call")

        Ctor.inst().add_method(T, False, True)
        
        return _impfunc_impl
     
def impfunc(*args, **kwargs):
    """Marks an imported function"""
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        # No-argument form
        return _impfunc({})(args[0])
    else:
        return _impfunc(kwargs)
    
class _expfunc(object):
    
    def __init__(self, kwargs):
        pass
    
    def __call__(self, T):
        # TODO: will need a way to hook the method
        def _expfunc_impl(self, *args, **kwargs):
            ifinst_data = self._ifinst_data
            print("_expfunc_impl: is_mirror=%s" % (str(ifinst_data.is_mirror)))
            
            if self._ifinst_data.is_mirror:
                # This is actually an import, since it's a mirror
                print("TODO: queue method call")
            else:
                # This is actually an export. It should be okay to
                # invoke it directly
                T(self, *args, **kwargs)
                
        Ctor.inst().add_method(T, False, False)
        return _expfunc_impl
    
def expfunc(*args, **kwargs):
    """Marks an exported function"""
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        # No-argument form
        return _expfunc({})(args[0])
    else:
        return _expfunc(kwargs)

class _imptask(object):
    
    def __init__(self, kwargs):
        pass
    
    def __call__(self, T):
        async def _imptask_impl(self, *args, **kwargs):
            # TODO: how do we find the proper endpoint?
            pass
        Ctor.inst().add_method(T, True, True)
        return _imptask_impl
    
def imptask(*args, **kwargs):
    """Marks an imported task"""
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        # No-argument form
        return _imptask({})(args[0])
    else:
        return _imptask(kwargs)

class _exptask(object):
    
    def __init__(self, kwargs):
        pass
    
    def __call__(self, T):
        # TODO: will need a way to hook the method

        method_t = Ctor.inst().add_method(T, False, False)
        
        async def _exptask_impl(self, *args, **kwargs):
            ifinst_data = self._ifinst_data
            print("_exptask_impl: is_mirror=%s" % (str(ifinst_data.is_mirror)))
            
            if self._ifinst_data.is_mirror:
                # This is actually an import, since it's a mirror
                print("TODO: queue method call")
                print("method_t: %s" % str(method_t))
                print("ifinst: %s" % str(ifinst_data.ifinst))
                if ifinst_data.ep not in method_t.method_t_ep_m.keys():
                    raise Exception("Endpoint not supported")
                ep_method_t = method_t.method_t_ep_m[ifinst_data.ep]
                params = ParamPacker(ifinst_data.ep, ep_method_t).pack(*args, *kwargs)

                ev = tblink.Event()
                retval = None
                
                def completion_f(rv):
                    nonlocal retval, ev
                    retval = rv
                    ev.set()
                
                ifinst_data.ifinst.invoke(
                    # TODO: method_t is endpoint-specific
                    ep_method_t,
                    params,
                    completion_f)

                if not ev.is_set():                
                    await ev.wait()
                    
                # TODO: Need to unpack return
                ret = None
                
                return ret
            else:
                # This is actually an export. It should be okay to
                # invoke it directly
                return await T(self, *args, **kwargs)
                
        return _exptask_impl
    
def exptask(*args, **kwargs):
    """Marks an exported function"""
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        # No-argument form
        return _exptask({})(args[0])
    else:
        return _exptask(kwargs)


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

class IfInstData(object):
    
    def __init__(self, ep, inst_name, is_mirror):
        self.ep = ep
        self.inst_name = inst_name
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

            ret._ifinst_data = IfInstData(_ep, _inst_name, False)

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

            ret._ifinst_data = IfInstData(_ep, _inst_name, True)

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
    
class _impfunc_i(object):
    
    def __init__(self, T):
        self.T = T
        self.mirror_T = None
        pass

    @staticmethod    
    def __call__(*args, **kwargs):
        print("_impfunc_i::call %s %s" % (str(args), str(kwargs)))
        pass
    
    def mirror(self, T):
        # T is the method to invoke for a mirror
        
        def stub(*args, **kwargs):
            raise Exception("Mirror for method %s may not be directly invoked" % self.T.__name__)
            print("stub")
            
        self.mirror_T = T
        print("mirror: %s" % str(T))
        
        return stub
    
class _impfunc(object):
      
    def __init__(self, kwargs):
        pass
      
    def __call__(self, T):
        # Must capture the function for use in the
        # mirror case.
        def _impfunc_impl(self, *args, **kwargs):
            pass
        Ctor.inst().add_method(T, False, True)
        return _impfunc_i(T)
     
def impfunc(*args, **kwargs):
    """Marks an imported function"""
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        # No-argument form
        return _impfunc({})(args[0])
    else:
        return _impfunc(kwargs)
    
class _expfunc_i(object):
    
    def __init__(self, T):
        self.T = T
        pass
    
    def __call__(self, *args, **kwargs):
        print("expfunc_i: %s args=%s" % (str(self.T), str(args)))
        pass
    
    def mirror(self, T):
        print("mirror: %s" % str(T))

class _expfunc(object):
    
    def __init__(self, kwargs):
        pass
    
    def __call__(self, T):
        # TODO: will need a way to hook the method
        def exp_func(*args, **kwargs):
            print("exp_func: %s %s" % (str(args), str(kwargs)))
        Ctor.inst().add_method(T, False, False)
        return exp_func
    
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


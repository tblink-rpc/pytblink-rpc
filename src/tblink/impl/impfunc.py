'''
Created on Sep 7, 2021

@author: mballance
'''
import tblink
from tblink.impl.ctor import Ctor
from tblink.impl.param_packer import ParamPacker
from tblink.impl.unpacker import Unpacker


class impfunc(object):
    """Implementation of the 'tblink.impfunc' decorator"""
      
    def __init__(self, kwargs):
        pass
      
    def __call__(self, T):
        method_t = Ctor.inst().add_method(T, False, False)
        
        # Must capture the function for use in the
        # mirror case.
        def _impfunc_impl(self, *args, **kwargs):
            ifinst_data = self._ifinst_data
            
            if ifinst_data.is_mirror:
                # This is actually an export, since the ifinst is a mirror
                # It should be okay to invoke it directly.
                return T(self, *args, **kwargs)                 
            else:
                # This is a true import, so we need to queue the
                # call and send it to the other side
                if ifinst_data.ep not in method_t.method_t_ep_m.keys():
                    raise Exception("Endpoint not supported")
                ep_method_t = method_t.method_t_ep_m[ifinst_data.ep]
                params = ParamPacker(ifinst_data.ep, ep_method_t).pack(*args, *kwargs)

                is_complete = False
                retval = None
                
                def completion_f(rv):
                    nonlocal retval, is_complete
                    retval = rv
                    is_complete = True
                
                ifinst_data.ifinst.invoke(
                    # TODO: method_t is endpoint-specific
                    ep_method_t,
                    params,
                    completion_f)

                # TODO: how do we spin until receiving a response?
#                if not ev.is_set():
#                    await ev.wait()
                    
                # TODO: Need to unpack return
                if not is_complete:
                    raise Exception("TODO: need to busy-wait for split response")
                
                ret = None
                if retval is not None:
                    ret = Unpacker().unpack_val(
                        retval,
                        ep_method_t.rtype)
                    
                return ret                

        
        return _impfunc_impl
    
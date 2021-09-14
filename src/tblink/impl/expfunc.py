'''
Created on Sep 7, 2021

@author: mballance
'''
from tblink.impl.ctor import Ctor
from tblink.impl.param_packer import ParamPacker
from tblink.impl.unpacker import Unpacker


class expfunc(object):
    
    def __init__(self, kwargs):
        pass
    
    def __call__(self, T):
        method_t = Ctor.inst().add_method(T, True, False)
        
        # TODO: will need a way to hook the method
        def _expfunc_impl(self, *args, **kwargs):
            ifinst_data = self._ifinst_data
            
            if self._ifinst_data.is_mirror:
                # This is actually an import, since it's a mirror
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
                    
                while not is_complete:
                    ifinst_data.ep.process_one_message()
                
                # Pack return value if provided
                ret = None
                if retval is not None:
                    ret = Unpacker().unpack_val(
                        retval,
                        ep_method_t.rtype)
                    
                return ret
            else:
                # This is actually an export. It should be okay to
                # invoke it directly
                return T(self, *args, **kwargs)
                
        return _expfunc_impl
    
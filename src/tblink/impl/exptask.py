'''
Created on Sep 7, 2021

@author: mballance
'''
import tblink
from tblink.impl.ctor import Ctor
from tblink.impl.param_packer import ParamPacker


class exptask(object):
    """Implementation for the 'tblink.exptask' decorator"""
    
    def __init__(self, kwargs):
        pass
    
    @staticmethod
    async def _exptask_impl(self, *args, **kwargs):
        pass
    
    def __call__(self, T):
        # TODO: will need a way to hook the method

        method_t = Ctor.inst().add_method(T, False, True)
        
        async def _exptask_impl(self, *args, **kwargs):
            ifinst_data = self._ifinst_data
            print("_exptask_impl: is_mirror=%s" % (str(ifinst_data.is_mirror)))
            
            if self._ifinst_data.is_mirror:
                # This is actually an import, since it's a mirror
                if ifinst_data.ep not in method_t.method_t_ep_m.keys():
                    raise Exception("Endpoint not supported")
                ep_method_t = method_t.method_t_ep_m[ifinst_data.ep]
                params = ParamPacker(ifinst_data.ep, ep_method_t).pack(*args, *kwargs)

                ev = tblink.Event()
                retval = None
                
                def completion_f(rv):
                    nonlocal retval, ev
                    print("--> completion_f", flush=True)
                    retval = rv
                    ev.set()
                    print("<-- completion_f", flush=True)
                
                ifinst_data.ifinst.invoke(
                    # TODO: method_t is endpoint-specific
                    ep_method_t,
                    params,
                    completion_f)

                print("--> await completion", flush=True)
                if not ev.is_set():
                    await ev.wait()
                print("<-- await completion", flush=True)
                    
                # TODO: Need to unpack return
                ret = None
                
                return ret
            else:
                # This is actually an export. It should be okay to
                # invoke it directly
                return await T(self, *args, **kwargs)
                
        return _exptask_impl
    
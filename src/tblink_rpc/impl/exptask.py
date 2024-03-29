'''
Created on Sep 7, 2021

@author: mballance
'''
import tblink_rpc
from tblink_rpc.impl.ctor import Ctor
from tblink_rpc.impl.param_packer import ParamPacker
from tblink_rpc.impl.unpacker import Unpacker
from tblink_rpc_core.tblink import TbLink
import traceback


class exptask(object):
    """Implementation for the 'tblink.exptask' decorator"""
    
    def __init__(self, kwargs):
        pass
    
    @staticmethod
    async def _exptask_impl(self, *args, **kwargs):
        pass
    
    def __call__(self, T):
        # TODO: will need a way to hook the method

        method_t = Ctor.inst().add_method(T, True, True)
        
        async def _exptask_impl(self, *args, **kwargs):
            ifinst_data = self._ifinst_data
            print("_exptask_impl", flush=True)

            try:            
                if self._ifinst_data.is_mirror:
                    # This is actually an import, since it's a mirror
                    if ifinst_data.backend.ep() not in method_t.method_t_ep_m.keys():
                        raise Exception("Endpoint not supported")
                    ep_method_t = method_t.method_t_ep_m[ifinst_data.backend.ep()]
                    params = ParamPacker(ifinst_data.backend.ep(), ep_method_t).pack(*args, *kwargs)
    
                    ev = ifinst_data.backend.event()
                    retval = None
                    
                    def completion_f(rv):
                        nonlocal retval, ev
                        print("--> completion_f", flush=True)
                        retval = rv
                        ev.set()
                        print("<-- completion_f", flush=True)
    
                    print("_exptask_impl: ifinst=%s" % str(type(ifinst_data.ifinst)))                
                    ifinst_data.ifinst.invoke(
                        # TODO: method_t is endpoint-specific
                        ep_method_t,
                        params,
                        completion_f)
    
                    if not ev.is_set():
                        print("--> wait for event", flush=True)
                        await ev.wait()
                        print("<-- wait for event", flush=True)
                        
                    # TODO: Need to unpack return
                    ret = None
                    
                    if retval is not None:
                        ret = Unpacker().unpack_val(
                            retval,
                            ep_method_t.rtype)
                        
                    return ret
                else:
                    print("_exptask_impl: non-mirror", flush=True)
                    # This is actually an export. It should be okay to
                    # invoke it directly
                    return await T(self, *args, **kwargs)
            except Exception as e:
                print("ExpTask Exception: %s" % str(e))
                traceback.print_exc()
                raise e
                
        return _exptask_impl
    

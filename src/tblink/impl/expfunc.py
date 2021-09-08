'''
Created on Sep 7, 2021

@author: mballance
'''
from tblink.impl.ctor import Ctor


class expfunc(object):
    
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
    
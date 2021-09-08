'''
Created on Sep 7, 2021

@author: mballance
'''
from tblink.impl.ctor import Ctor


class impfunc(object):
    """Implementation of the 'tblink.impfunc' decorator"""
      
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
    
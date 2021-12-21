'''
Created on Sep 7, 2021

@author: mballance
'''
from tblink.impl.ctor import Ctor


class imptask(object):
    """Implementation of the 'tblink.imptask' decorator"""
    
    def __init__(self, kwargs):
        pass
    
    def __call__(self, T):
        async def _imptask_impl(self, *args, **kwargs):
            # TODO: how do we find the proper endpoint?
            pass
        Ctor.inst().add_method(T, True, True)
        return _imptask_impl
'''
Created on Mar 7, 2021

@author: mballance
'''

class Backend(object):
    """Defines backend API required to interact with simulation"""
    
    def __init__(self):
        pass
    
    def simtime(self) -> int:
        """Returns simtime with default units and precision"""
        raise NotImplementedError("simtime not implemented")
    
    def add_simtime_cb(self, cb, time):
        raise NotImplementedError("add_simtime_cb not implemented")
    
    def get_timeunit(self) -> int:
        """Returns unit"""
        raise NotImplementedError("get_timeunit not implemented")
    
    def get_timeprecision(self) -> int:
        """Returns precision -- 0, -3, -6, -9, -12..."""
        raise NotImplementedError("get_timeprecision not implemented")
    
    def get_ctxt(self, key):
        raise NotImplementedError("get_ctxt not implemented")
    
    def call(self, name, ctxt, argtypes, args):
        raise NotImplementedError("call not implemented")
    
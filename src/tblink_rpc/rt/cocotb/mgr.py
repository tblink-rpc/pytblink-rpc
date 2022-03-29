'''
Created on Jan 22, 2022

@author: mballance
'''
from tblink_rpc_core.endpoint import Endpoint
import traceback

class CbClosure(object):
    
    def __init__(self, ep, cb_id):
        self.ep = ep
        self.cb_id = cb_id
        
    def deregister(self):
        self.ep.cancel_callback(self.cb_id)

class Mgr(object):
    
    _inst = None
    
    def __init__(self):
        self.ep : Endpoint = None
        
    def stop_simulator(self):
        self.ep.shutdown()
        
    def get_sim_time(self):
        time = self.ep.time()
        return ((time >> 32), time & 0xFFFFFFFF)
    
    def get_precision(self):
        p = int(self.ep.time_precision())
        return p
    
    def register_timed_callback(self, t, cb, ud):
        def callback():
            print("Callback Triggered", flush=True)
            try:
                cb(ud)
            except Exception as e:
                print("Exception: %s" % str(e))
                traceback.print_exc()

        ret = CbClosure(self.ep, self.ep.add_time_callback(
            t, lambda : cb(ud)))
        return ret
        
    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = Mgr()
        return cls._inst
    
    @classmethod
    def init(cls):
        cls._inst = Mgr()
        return cls._inst
            
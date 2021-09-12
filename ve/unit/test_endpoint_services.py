'''
Created on Sep 11, 2021

@author: mballance
'''
from typing import List

from tblink_rpc_core.endpoint import Endpoint, TimeUnit
from tblink_rpc_core.endpoint_services import EndpointServices


class TestEndpointServices(EndpointServices):
    
    def __init__(self, args):
        self._args = args.copy()
        pass

    def init(self, ep : Endpoint):
        pass
    
    def args(self) -> List[str]:
        return self._args
    
    def shutdown(self): 
        pass
    
    def add_time_cb(self, time, callback_id) -> int:
        pass
    
    def cancel_callback(self, callback_id):
        pass
    
    def time(self) -> int:
        return 0
    
    def time_precision(self) -> int:
        return TimeUnit.ns
    
    def run_until_event(self):
        pass
    
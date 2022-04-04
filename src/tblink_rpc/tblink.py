'''
Created on Mar 9, 2021

@author: mballance
'''
import asyncio
from asyncio.coroutines import iscoroutine
import inspect
from asyncio import Task
from tblink_rpc.backend import Backend
import tblink_rpc_core
from tblink_rpc_core.launch_type import LaunchType
from tblink_rpc_core.endpoint import Endpoint

class TbLink(object):
    
    _tblink = None
    
    def __init__(self):
        self.dflt_backend : Backend = None
        self.tblink_core = tblink_rpc_core.tblink.TbLink.inst()
        self._endpoints = []
        self._ep2backend_m = {}
    
    @classmethod
    def inst(cls):
        if cls._tblink is None:
            cls._tblink = TbLink()
        return cls._tblink
    
    def getDefaultEP(self):
        if self.tblink_core is not None:
            return self.tblink_core.getDefaultEP()
        else:
            return None
        
    def addEndpoint(self, ep, backend):
        if self.dflt_backend is None:
            self.dflt_backend = backend
        self._endpoints.append(ep)
        self._ep2backend_m[ep] = backend
        
    def removeEndpoint(self, ep):
        self._endpoints.remove(ep)
        self._ep2backend_m.pop(ep)
        
    def getEndpoints(self):
        ret = self._endpoints.copy()
        ret.extend(self.tblink_core.getEndpoints())
        return ret
    
    def getBackend(self, ep : Endpoint):
        if ep not in self._ep2backend_m.keys():
            return self.dflt_backend
        else:
            return self._ep2backend_m[ep]
        
    def findLaunchType(self, name) -> LaunchType:
        return self.tblink_core.findLaunchType(name)
    
    @classmethod
    def test_init(cls):
        cls._tblink = None
    
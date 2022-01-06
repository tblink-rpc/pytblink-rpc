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

class TbLink(object):
    
    _tblink = None
    
    def __init__(self):
        self.dflt_backend : Backend = None
        self.tblink_core = tblink_rpc_core.tblink.TbLink.inst()
    
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
        
    def findLaunchType(self, name) -> LaunchType:
        return self.tblink_core.findLaunchType(name)
    
    @classmethod
    def test_init(cls):
        cls._tblink = None
    
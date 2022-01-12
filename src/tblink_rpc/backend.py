'''
Created on Mar 7, 2021

@author: mballance
'''
from typing import List
from tblink_rpc.event import Event
from tblink_rpc.lock import Lock
from tblink_rpc.condition import Condition
from tblink_rpc.task import Task
from .time_unit import TimeUnit
from tblink_rpc_core.endpoint import Endpoint

class Backend(object):
    """Defines API for interacting with environment"""
    
    def ep(self) -> Endpoint:
        """Returns the endpoint used by this backend"""
        raise NotImplementedError("ep not implemented")
   
    def findPeerIfinst(self, name):
        """Finds peer interface instances matching a name pattern"""
        raise NotImplementedError("findPeerIfinst not implemented")
    
    def findPeerIfinsts(self, name):
        """Finds peer interface instances matching a name pattern"""
        raise NotImplementedError("findPeerIfinst not implemented")
    
    def args(self) -> List[str]:
        """Returns the list of command-line arguments"""
        raise NotImplementedError("args not implemented")
    
    def time(self) -> int:
        """Returns time with default units and precision"""
        raise NotImplementedError("time not implemented by %s" % str(type(self)))
    
    def timeunit(self) -> int:
        """Returns unit"""
        raise NotImplementedError("timeunit not implemented")
    
    def start_soon(self, coro) -> Task:
        raise NotImplementedError("start_soon not implemented")
    
    async def gather(self, *aws):
        raise NotImplementedError("gather not implemented")
    
    def timeprecision(self) -> int:
        """Returns precision -- 0, -3, -6, -9, -12..."""
        raise NotImplementedError("get_timeprecision not implemented")
    
    def condition(self) -> Condition:
        raise NotImplementedError("condition not implemented by %s" % str(type(self)))
    
    def event(self) -> Event:
        raise NotImplementedError("event not implemented by %s" % str(type(self)))
    
    def lock(self) -> Lock:
        raise NotImplementedError("lock not implemented by %s" % str(type(self)))
    
    async def sleep(self, time, unit=None):
        raise NotImplementedError("sleep not implemented by %s" % str(type(self)))
    
    def timer(self, time, unit=None) -> Event:
        raise NotImplementedError("timer not implemented by %s" % str(type(self)))
    
    def mkInst(self, T, inst_name, *args, **kwargs):
        """Creates an interface instance"""
        raise NotImplementedError("mkInst not implemented by %s" % str(type(self)))
    
    def mkMirrorInst(self, T, inst_name, *args, **kwargs):
        """Creates a mirror interface instance"""
        raise NotImplementedError("mkMirrorInst not implemented by %s" % str(type(self)))
        

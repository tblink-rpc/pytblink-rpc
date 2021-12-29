'''
Created on Dec 27, 2021

@author: mballance
'''
import asyncio
from typing import List

from tblink_rpc.backend import Backend
from tblink_rpc.condition import Condition
from tblink_rpc.event import Event
from tblink_rpc.lock import Lock
from tblink_rpc.rt.task_asyncio import TaskAsyncio
from tblink_rpc.task import Task
from tblink_rpc_core.endpoint import Endpoint
import re


class BackendAsyncio(Backend):
    
    def __init__(self, ep):
        self._ep = ep
        
    def ep(self) -> Endpoint:
        """Returns the endpoint used by this backend"""
        return self._ep
    
    def findPeerIfinst(self, name):
        """Finds peer interface instances matching a name pattern"""
        match_if = self.findPeerIfinsts(name)
        if len(match_if) == 1:
            return match_if[0]
        elif len(match_if) > 1:
            raise Exception("Pattern %s matched %d instances" % (name, len(match_if)))
        else:
            return None
    
    def findPeerIfinsts(self, name):
        """Finds peer interface instances matching a name pattern"""
        ret = []
        name_p = re.compile(name)
        
        for ifinst in self._ep.getPeerInterfaceInsts():
            print("IFINST: %s" % ifinst.name())
            if name_p.match(ifinst.name()):
                ret.append(ifinst)
        return ret
        
    def args(self) -> List[str]:
        """Returns the list of command-line arguments"""
        return self._ep.args()
    
    def time(self) -> int:
        """Returns time with default units and precision"""
        return self._ep.time()
    
    def add_time_cb(self, cb, time, unit=None):
        # TODO: convert time units if needed
        self._ep.add_time_callback(time, cb)
    
    def timeunit(self) -> int:
        """Returns unit"""
        raise NotImplementedError("timeunit not implemented")
    
    def start_soon(self, coro) -> Task:
        return TaskAsyncio(asyncio.ensure_future(coro))
    
    def timeprecision(self) -> int:
        """Returns precision -- 0, -3, -6, -9, -12..."""
        raise NotImplementedError("get_timeprecision not implemented")
    
    def condition(self) -> Condition:
        return asyncio.Condition()
    
    def event(self) -> Event:
        return asyncio.Event()
    
    def lock(self) -> Lock:
        return asyncio.Lock()
    
    async def sleep(self, time, unit=None):
        await self.timer(time, unit).wait()
    
    def timer(self, time, unit=None) -> Event:
        ev = self.event()
        
        def _cb():
            nonlocal ev
            ev.set()
        # TODO: scale time
        self._ep.add_time_callback(time, _cb)
        
        return ev
    
    def mkInst(self, T, inst_name, *args, **kwargs):
        """Creates an interface instance"""
        raise NotImplementedError("mkInst not implemented by %s" % str(type(self)))
    
    def mkMirrorInst(self, T, inst_name, *args, **kwargs):
        """Creates a mirror interface instance"""
        raise NotImplementedError("mkMirrorInst not implemented by %s" % str(type(self)))
    
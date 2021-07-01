'''
Created on Mar 9, 2021

@author: mballance
'''
import asyncio
from asyncio.coroutines import iscoroutine
import inspect
from asyncio import Task
from tblink.backend import Backend

class TbLink(object):
    
    _tblink = None
    
    def __init__(self, backend):
        self.backend : Backend = backend
        self.loop = asyncio.get_event_loop()
        self.is_running = False
        self.entry_f = None
        self.entry_t = None
        TbLink._tblink = self
        
        self.units = backend.get_timeunit()
        self.precision = backend.get_timeprecision()
    
    @classmethod
    def inst(cls):
        return cls._tblink
    
    async def __entry_wrapper(self):
        await self.entry_f(None)
        self.is_running = False
        pass
    
    def start(self, entry_f):
        if not iscoroutine(entry_f) and not inspect.isawaitable(entry_f) and not inspect.iscoroutinefunction(entry_f):
            raise Exception("Entry method " + str(entry_f) + " is not awaitable")
        
        self.is_running = True
        self.entry_f = entry_f
        self.entry_t = asyncio.ensure_future(self.__entry_wrapper())
        pass
    
    def __end_reschedule(self):
        """Allows us to stop the event loop after processing all pending events"""
        self.loop.stop()
    
    def reschedule(self) -> bool:
        """Runs the event loop. Returns 'true' while still running"""
        
        self.loop.call_soon(self.__end_reschedule)
        self.loop.run_forever()
        
        return self.is_running
    
    async def sleep(self, time, units=None):
        e = asyncio.Event()
        
        def _notify():
            nonlocal e
            e.set()
            
        if units is None:
            units = self.units

        unscaled = time
        if units > self.units:
            # Desired units are coarser than default
            unscaled *= (10 ** (units-self.units))
        elif units < self.units:
            # Desired units are finer than default
            unscaled /= (10 ** (units-self.units))
            
        self.backend.add_simtime_cb(unscaled, _notify)
        await e.wait()
    
    def simtime(self, units=None) -> int:
        if units is None:
            units = self.units
            
        unscaled = self.backend.simtime()

        if units > self.units:
            # Desired units are coarser than default
            unscaled /= (10 ** (units-self.units))
        elif units < self.units:
            # Desired units are finer than default
            unscaled *= (10 ** (units-self.units))
        
        return unscaled
        
    
    async def __task_wrapper(self, coro):
        print("-- task_wrapper")
        try:
            await coro
        except Exception as e:
            print("Exception: " + str(e))
        pass
    
    def fork(self, coro) -> Task:
        if not iscoroutine(coro) and not inspect.isawaitable(coro) and not inspect.iscoroutinefunction(coro):
            raise Exception("Entry method " + str(coro) + " is not awaitable")
        return asyncio.ensure_future(self.__task_wrapper(coro))
    
    @classmethod
    def test_init(cls):
        cls._tblink = None
    
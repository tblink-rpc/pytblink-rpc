#****************************************************************************
#* tblink
#****************************************************************************

from .decorators import *
from tblink.backend import Backend
from tblink.tblink import TbLink
import importlib
import asyncio
from asyncio import Task
import sys
import os
from enum import IntEnum
from tblink.impl.backend_asyncio import BackendAsyncio

_backend = None

def _get_backend():
    global _backend
    
    if _backend is None:
        _backend = BackendAsyncio()
    return _backend

class TimeUnit(IntEnum):
    ps = -12
    ns = -9
    us = -6
    ms = -3
    s = 0
    
    @classmethod
    def str2unit(cls, unit_s):
        if unit_s == "ps":
            return cls.ps
        elif unit_s == "ns":
            return cls.ns
        elif unit_s == "us":
            return cls.us
        elif unit_s == "ms":
            return cls.ms
        elif unit_s == "s":
            return cls.s
        else:
            raise Exception("Unknown type unit \"%s\"" % unit_s)
    
    
def init(
        backend : Backend,
        module : str = None):
    """Called by the launcher to initialize the tblink package with a backend."""
    
    TbLink(backend)
    
    if module is not None:
        try:
            m = importlib.import_module(module)
        except Exception as e:
            print("Failed to load module \"" + module + "\": " + str(e))
            raise e
    else:
        if "MODULE" in os.environ.keys():
            importlib.import_module(os.environ["MODULE"])
        else:
            raise Exception("No module specified for loading")
    
    pass

def Event():
    return _get_backend().event()

def fork(coro) -> Task:
    return _get_backend().fork(coro)

def Lock():
    return _get_backend().lock()

def simtime(units=None):
    if units is not None:
        if isinstance(units, str):
            units = TimeUnit.str2unit(units)
    return TbLink.inst().simtime(units)

async def sleep(time, units=None):
    if units is not None:
        if isinstance(units, str):
            units = TimeUnit.str2unit(units)
    await TbLink.inst().sleep(time, units)
            
def test_init():
    """Called by unit tests to clear state of the package"""
    
    TbLink.test_init()
    TestRgy.test_init()
    Ctor.reset()
    
    # TODO: clear out test registry
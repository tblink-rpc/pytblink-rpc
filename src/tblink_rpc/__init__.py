#****************************************************************************
#* tblink
#****************************************************************************

from .decorators import *
from tblink_rpc.backend import Backend
from tblink_rpc.tblink import TbLink
import importlib
import asyncio
from asyncio import Task
import sys
import os
from enum import IntEnum
from tblink_rpc.impl.backend_asyncio import BackendAsyncio
from .time_unit import *
import tblink_rpc_core

    
def event():
    return TbLink.inst().dflt_backend.event()

def start_soon(coro) -> Task:
    return TbLink.inst().dflt_backend.start_soon(coro)

async def gather(*aws):
    await TbLink.inst().dflt_backend.gather(*aws)

def lock():
    return TbLink.inst().dflt_backend.lock()

async def sleep(time, unit=None):
    await TbLink.inst().dflt_backend.sleep(time, unit)

def test_init():
    """Called by unit tests to clear state of the package"""
    TbLink.test_init()
    
'''
Created on Jul 8, 2020

@author: ballance
'''

import ctypes
from typing import Generic, TypeVar, List
import typing

import tblink
from .impl.iftype import iftype as iftype_impl
from .impl.impfunc import impfunc as impfunc_impl
from .impl.imptask import imptask as imptask_impl
from .impl.expfunc import expfunc as expfunc_impl
from .impl.exptask import exptask as exptask_impl

from tblink.impl.ctor import Ctor
from tblink.impl.ifinst_data import IfInstData
from tblink.impl.iftype_decl import IftypeDecl
from tblink.impl.iftype_rgy import IftypeRgy
from tblink.impl.param_packer import ParamPacker
from tblink_rpc_core.endpoint_mgr import EndpointMgr

from .impl.test_rgy import TestRgy


def iftype(*args, **kwargs):
    """Marks an interface type"""
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        # No-argument form
        return iftype_impl({})(args[0])
    else:
        return iftype_impl(kwargs)
    
def impfunc(*args, **kwargs):
    """Marks an imported function"""
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        # No-argument form
        return impfunc_impl({})(args[0])
    else:
        return impfunc_impl(kwargs)
    
def expfunc(*args, **kwargs):
    """Marks an exported function"""
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        # No-argument form
        return expfunc_impl({})(args[0])
    else:
        return expfunc_impl(kwargs)
    
def imptask(*args, **kwargs):
    """Marks an imported task"""
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        # No-argument form
        return imptask_impl({})(args[0])
    else:
        return imptask_impl(kwargs)

def exptask(*args, **kwargs):
    """Marks an exported function"""
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        # No-argument form
        return exptask_impl({})(args[0])
    else:
        return exptask_impl(kwargs)


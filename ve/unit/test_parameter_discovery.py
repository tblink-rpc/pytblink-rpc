'''
Created on Jan 13, 2021

@author: mballance
'''
import ctypes
from typing import List, Dict
from unittest.case import TestCase

import tblink
from tblink.impl.iftype_rgy import IftypeRgy
from tblink.model.method_type import MethodType
from tblink.model.type_decl import TypeDeclE


class TestParameterDiscovery(TestCase):
    
    def test_1(self):
        
        @tblink.iftype(name="foo.bar.if")
        class T(object):
            
            def __init__(self):
                pass
            
            @tblink.impfunc
            def imp(self, a : ctypes.c_uint64, b : ctypes.c_uint32, c : str, d : List[ctypes.c_uint32]):
                pass
            
            @tblink.impfunc
            def my_func2(self, a : Dict[str,ctypes.c_uint32]):
                pass

        iftype = IftypeRgy.inst().find_iftype("foo.bar.if")
        self.assertIsNotNone(iftype)
        
        imp_m : MethodType = iftype.find_method("imp")
        self.assertIsNotNone(imp_m)
        
        self.assertTrue(imp_m.is_import)
        self.assertFalse(imp_m.is_task)
        
        self.assertEqual(len(imp_m.params), 4)
        
        self.assertEqual(imp_m.params[0].ptype.base_t, TypeDeclE.u64)
        self.assertEqual(imp_m.params[1].ptype.base_t, TypeDeclE.u32)
        self.assertEqual(imp_m.params[2].ptype.base_t, TypeDeclE.str)
        self.assertEqual(imp_m.params[3].ptype.base_t, TypeDeclE.vec)
        self.assertEqual(imp_m.params[3].ptype.elem_t.base_t, TypeDeclE.u32)
        
#        i = T()
#        i.imp(1, 2)
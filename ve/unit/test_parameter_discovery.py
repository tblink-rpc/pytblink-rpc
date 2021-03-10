'''
Created on Jan 13, 2021

@author: mballance
'''
import tblink
from unittest.case import TestCase
import ctypes

class TestParameterDiscovery(TestCase):
    
    def test_1(self):

        @tblink.imp_task
        def imp(a : ctypes.c_uint64, b : ctypes.c_uint32):
            pass
        
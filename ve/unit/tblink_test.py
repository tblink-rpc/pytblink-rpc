'''
Created on Mar 9, 2021

@author: mballance
'''
from unittest.case import TestCase
import tblink
from test_backend import TestBackend
from tblink.tblink import TbLink

class TblinkTest(TestCase):
    
    def setUp(self):
        tblink.test_init()
        tblink.init(TestBackend())
    
    def tearDown(self):
        tblink.test_init()
        
    def runTest(self, entry_f=None):
        tblink.start()

        i = 0
        limit = 1000000        
        while i < limit:
            if not TbLink.inst().backend.run():
                break
            i += 1
            
        if i >= limit:
            raise Exception("Timeout")
        
        
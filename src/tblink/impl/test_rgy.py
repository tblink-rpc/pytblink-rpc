'''
Created on Mar 8, 2021

@author: mballance
'''

class TestRgy(object):
    
    _inst = None
    
    def __init__(self):
        self.tests = []
        pass
    
    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = TestRgy()
        return cls._inst
    
    def add_test(self, t):
        self.tests.append(t)
        
    @classmethod
    def test_init(cls):
        cls._inst = None
        
        
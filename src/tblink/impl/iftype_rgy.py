'''
Created on Aug 22, 2021

@author: mballance
'''

class IftypeRgy(object):
    
    _inst = None
    
    def __init__(self):
        pass
    
    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = IftypeRgy()
        return cls._inst
    
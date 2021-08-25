'''
Created on Aug 22, 2021

@author: mballance
'''

class IftypeRgy(object):
    
    _inst = None
    
    def __init__(self):
        self.iftypes = []
        self.iftype_m = {}
        pass
    
    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = IftypeRgy()
        return cls._inst
    
    def add_iftype(self, iftype):
        if iftype.name in self.iftype_m.keys():
            raise Exception("Duplicate iftype %s" % iftype.name)
        self.iftypes.append(iftype)
        self.iftype_m[iftype.name] = iftype
    
    def find_iftype(self, name):
        if name in self.iftype_m.keys():
            return self.iftype_m[name]
        else:
            return None
'''
Created on Aug 24, 2021

@author: mballance
'''

class InterfaceType(object):
    
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods
        self.method_m = {}
        for m in methods:
            self.method_m[m.name] = m
            
    def find_method(self, name):
        if name in self.method_m.keys():
            return self.method_m[name]
        else:
            return None
        
    
    
    
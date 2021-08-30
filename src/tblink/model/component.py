'''
Created on Aug 25, 2021

@author: mballance
'''

class Component(object):
    
    def __init__(self, parent, name):
        self.parent = parent
        self.children = []
        self.endpoint = None
        pass
    
    def _do_build(self, ep):
        self.endpoint = ep
        
        self.build()
        for c in self.children:
            c._do_build(ep)
    
    def build(self):
        pass
    
    def _do_connect(self):
        
        for c in self.children:
            c._do_connect()
        self.connect()
    
    def connect(self):
        pass
    
    def _do_start(self):
        for c in self.children:
            c._do_start()
        self.start()
    
    def start(self):
        pass
    
    def mkInst(self, T, inst_name, *args, **kwargs):
        if not hasattr(T, "mkInst"):
            raise Exception("Type %s must be registered with @ifinst (missing mkInst method)" % str(type(T)))
        
        return T.mkInst(
            self.endpoint, 
            inst_name, 
            *args,
            *kwargs)
        
    def mkMirrorInst(self, T, inst_name, *args, **kwargs):
        if not hasattr(T, "mkMirrorInst"):
            raise Exception("Type %s must be registered with @ifinst (missing mkMirrorInst method)" % str(type(T)))
        
        return T.mkMirrorInst(
            self.endpoint, 
            inst_name, 
            *args,
            *kwargs)
    
    
'''
Created on Aug 25, 2021

@author: mballance
'''

class Component(object):
    
    def __init__(self, parent, name):
        self.parent = parent
        self.children = []
        self.endpoint = None
        self.objections = 0
        pass
    
    def _do_build(self, ep):
        self.endpoint = ep
        
        self.build(ep)
        for c in self.children:
            c._do_build(ep)
    
    def build(self, ep):
        pass
    
    def _do_connect(self, ep):
        
        for c in self.children:
            c._do_connect(ep)
        self.connect(ep)
    
    def connect(self, ep):
        pass
    
    def _do_start(self):
        for c in self.children:
            c._do_start()
        self.start()
    
    def start(self):
        pass
    
    def raise_objection(self):
        self.objections += 1
    
    def drop_objection(self):
        self.objections -= 1
        pass
    
    def _have_objections(self):
        return self.objections > 0
    
    async def sleep(self, time, unit):
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
    
    
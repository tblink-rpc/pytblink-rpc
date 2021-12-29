'''
Created on Aug 25, 2021

@author: mballance
'''

class Component(object):
    
    def __init__(self, parent, name):
        self._parent = parent
        self._children = []
        self._backend = None
        self._endpoint = None
        self._objections = 0
        pass
    
    def _do_build(self, backend, ep):
        self._backend = backend
        self._endpoint = ep
        
        self.build(ep)
        for c in self._children:
            c._do_build(backend, ep)
    
    def build(self, ep):
        pass
    
    def _do_connect(self, ep):
        for c in self._children:
            c._do_connect(ep)
        self.connect(ep)
    
    def connect(self, ep):
        pass
    
    def _do_start(self):
        for c in self._children:
            c._do_start()
        self._backend.start_soon(self.run())
    
    async def run(self):
        pass
    
    def raise_objection(self):
        self._objections += 1
    
    def drop_objection(self):
        self._objections -= 1
        pass
    
    def _have_objections(self):
        return self._objections > 0
    
    async def sleep(self, time, unit):
        pass
        
    
    def mkInst(self, T, inst_name, *args, **kwargs):
        if not hasattr(T, "mkInst"):
            raise Exception("Type %s must be registered with @iftype (missing mkInst method)" % str(type(T)))
        
        return T.mkInst(
            self._backend, 
            inst_name, 
            *args,
            *kwargs)
        
    def mkMirrorInst(self, T, inst_name, *args, **kwargs):
        if not hasattr(T, "mkMirrorInst"):
            raise Exception("Type %s must be registered with @iftype (missing mkMirrorInst method)" % str(type(T)))
        
        return T.mkMirrorInst(
            self._backend, 
            inst_name, 
            *args,
            *kwargs)
    
    
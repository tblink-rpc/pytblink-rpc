'''
Created on Aug 25, 2021

@author: mballance
'''
from TblinkTestCase import TblinkTestCase
from tblink.model.component import Component
import asyncio
from tblink_rpc_core.endpoint_msg_transport import EndpointMsgTransport
from tblink_rpc_core.transport_dual_fifo import TransportDualFifo
from tblink.runtime.runner import Runner
import ctypes
import tblink

class TestRunnerSmoke(TblinkTestCase):
    
    def smoke(self):

        # Must be able to express a 'mirror'
        # An instance is either the API or a mirror of the API
        # 
        # A class must be able to query whether it is of 
        # API or API-mirror type
        #
        @tblink.iftype(name="my_api")
        class Export(object):
            
            def __init__(self, v):
                print("Export.__init__: %s %d" % (self.inst_name(), v))
                self.send_f = None
                pass
            
            @tblink.expfunc
            def send_1(self, v : ctypes.c_uint32):
                if self.put_f is not None:
                    self.put_f(v)
                else:
                    print("put_f is None")
            
#            @send_1.mirror
#            def send_1(self, v : ctypes.c_uint32):
#                pass
            
            @tblink.impfunc
            def send_2(self, v : ctypes.c_uint32):
                print("send_2")
                pass
            
            @send_2.mirror
            def send_2_exp(self, v : ctypes.c_uint32):
                # Export implementation when 
                print("send_2.mirror")
                pass

        # What's the connection strategy? Require an endpoint up-front?
#        e = Export.mk("foo.bar.baz2", 2)

#        e.send_2(10)
#        e.send_1(10)
        
#        e2 = Export.mk("foo.bar.baz", 3)
        
#        e.send_2_exp(0)

        class C1(Component):
            
            def __init__(self, parent=None, name="C1"):
                super().__init__(parent, name)
                
            def build(self):
                print("C1 build")
                self.inst = self.mkInst(Export, "inst", 10)
                
            def connect(self):
                print("C1 connect")
                for ifinst in self.endpoint.peerInterfaceInsts():
                    print("  IfInst: %s" % ifinst.name)
                
            def start(self):
                print("C1.start", flush=True)
                asyncio.ensure_future(self.run())
                pass
                
            async def run(self):
                print("Run")
            
        class C2(Component):
            
            def __init__(self, parent=None, name="C2"):
                super().__init__(parent, name)
                
            def build(self):
                print("C2 build")
                self.inst = self.mkMirrorInst(Export, "inst", 10)
                
            def connect(self):
                print("C2 connect")
                for ifinst in self.endpoint.peerInterfaceInsts():
                    print("  IfInst: %s" % ifinst.name)
                
            def start(self):
                print("C2.start", flush=True)
                asyncio.ensure_future(self.run())
                
            async def run(self):
                print("Run")
                

        tp = TransportDualFifo()
        
        ep1 = EndpointMsgTransport(tp.ep[0])
        ep2 = EndpointMsgTransport(tp.ep[1])
        
        r1 = Runner(C1, ep1)
        r2 = Runner(C2, ep2)
        
#        rt1 = asyncio.ensure_future(r1.run())
#        rt2 = asyncio.ensure_future(r2.run())

        loop = asyncio.get_event_loop()
        
        print("--> Run", flush=True)
        loop.run_until_complete(asyncio.gather(
            r1.run(),
            r2.run()))
        print("<-- Run", flush=True)

        
'''
Created on Aug 25, 2021

@author: mballance
'''
from TblinkTestCase import TblinkTestCase
from tblink_rpc.component import Component
import asyncio
from tblink_rpc_core.endpoint_msg_transport import EndpointMsgTransport
from tblink_rpc_core.transport_dual_fifo import TransportDualFifo
from tblink_rpc.runtime.runner import Runner
import ctypes
import tblink
from test_endpoint_services import TestEndpointServices

class TestRunnerSmoke(TblinkTestCase):
    
    def smoke(self):
        import tblink.impl.cocotb as cocotb
        
        
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
                print("Hello from send_1")
            
#            @send_1.mirror
#            def send_1(self, v : ctypes.c_uint32):
#                pass
            
            @tblink.impfunc
            def send_2(self, v : ctypes.c_uint32):
                print("send_2")
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
                self.inst.send_1(1)
                self.inst.send_2(1)
            
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
                self.inst.send_1(1)
                self.inst.send_2(1)
                

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

    def test_sw_if(self):
        import tblink.impl.cocotb as cocotb
        
        testcase = self

        # Must be able to express a 'mirror'
        # An instance is either the API or a mirror of the API
        # 
        # A class must be able to query whether it is of 
        # API or API-mirror type
        #
        @tblink.iftype(name="my_api")
        class SwIf(object):
            
            def __init__(self):
                self.send_f = None
                self.call_counts = [0]*8
                pass
            
            @tblink.exptask
            async def write8(self, 
                             addr : ctypes.c_uint64,
                             data : ctypes.c_uint8):
                print("write8")
                self.call_counts[0] += 1
            
            @tblink.exptask
            async def write16(self, 
                             addr : ctypes.c_uint64,
                             data : ctypes.c_uint16):
                print("write16")
                self.call_counts[1] += 1
            
            @tblink.exptask
            async def write32(self, 
                             addr : ctypes.c_uint64,
                             data : ctypes.c_uint32):
                print("write32")
                self.call_counts[2] += 1
            
            @tblink.exptask
            async def write64(self, 
                             addr : ctypes.c_uint64,
                             data : ctypes.c_uint64):
                print("write64")
                self.call_counts[3] += 1

            @tblink.exptask
            async def read8(self, 
                             addr : ctypes.c_uint64) -> ctypes.c_uint8:
                print("read8")
                self.call_counts[4] += 1
                return addr + 1
            
            @tblink.exptask
            async def read16(self, 
                             addr : ctypes.c_uint64) -> ctypes.c_uint16:
                print("read16")
                self.call_counts[5] += 1
                return addr + 1
            
            @tblink.exptask
            async def read32(self, 
                             addr : ctypes.c_uint64) -> ctypes.c_uint32:
                print("read32")
                self.call_counts[6] += 1
                return addr + 1
            
            @tblink.exptask
            async def read64(self, 
                             addr : ctypes.c_uint64) -> ctypes.c_uint64:
                print("read64")
                self.call_counts[7] += 1
                return addr + 1
            
        class Sw(Component):
            """Represents the software process"""
            
            def __init__(self, parent=None, name="C1"):
                super().__init__(parent, name)
                
            def build(self):
                print("C1 build")
                testcase.assertEqual(len(self.endpoint.args()), 1)
                testcase.assertEqual(self.endpoint.args()[0], "b")
                self.api = self.mkMirrorInst(SwIf, "rw_api")
                
            def connect(self):
                print("C1 connect")
                for ifinst in self.endpoint.peerInterfaceInsts():
                    print("  IfInst: %s" % ifinst.name)
                
            def start(self):
                print("C1.start", flush=True)
                asyncio.ensure_future(self.run())
                pass
                
            async def run(self):
                print("--> Sw.Run")
                self.raise_objection()
                for i in range(10):
                    print("--> read8")
                    val = await self.api.read8(20+i)
                    print("<-- read8")
#                    testcase.assertEqual(val, 20+i+1)
                await self.api.write8(10, 10)
                self.drop_objection()
                print("<-- Sw.Run")
            
        class Host(Component):
            
            def __init__(self, parent=None, name="C2"):
                super().__init__(parent, name)
                self.inst = None
                
            def build(self):
                print("C2 build")
                
                testcase.assertEqual(len(self.endpoint.args()), 1)
                testcase.assertEqual(self.endpoint.args()[0], "a")
                # TODO: do we need the ability to specify the
                # implementation class for an interface?
                self.inst = self.mkInst(SwIf, "rw_api")
                
            def connect(self):
                print("C2 connect")
                for ifinst in self.endpoint.peerInterfaceInsts():
                    print("  IfInst: %s" % ifinst.name)
                
            def start(self):
                print("C2.start", flush=True)
                asyncio.ensure_future(self.run())
                
            async def run(self):
                print("Run")
#                self.inst.send_1(1)
#                self.inst.send_2(1)
                

        tp = TransportDualFifo()

        ep1 = EndpointMsgTransport(tp.ep[0])
        ep2 = EndpointMsgTransport(tp.ep[1])
        
        eps1 = TestEndpointServices(["a"])
        eps2 = TestEndpointServices(["b"])
        
        ep1.init(eps1, None)
        ep2.init(eps2, None)
        
        sw_i = Sw()
        host_i = Host()
        
        
        r1 = Runner(sw_i, ep1)
        r2 = Runner(host_i, ep2)
        
#        rt1 = asyncio.ensure_future(r1.run())
#        rt2 = asyncio.ensure_future(r2.run())

        loop = asyncio.get_event_loop()
        
        print("--> Run", flush=True)
        t1 = asyncio.ensure_future(r1.run())
        t2 = asyncio.ensure_future(r2.run())
        
        loop.run_until_complete(asyncio.gather(t1, t2))
        print("<-- Run", flush=True)
        
        print("t1.done: %s ; t2.done: %s" % (str(t1.done()), str(t2.done())))

        self.assertEqual(host_i.inst.call_counts[4], 10)
        self.assertEqual(host_i.inst.call_counts[0], 1)

    def test_cross_call(self):
        import tblink.impl.cocotb as cocotb
        
        testcase = self

        # Must be able to express a 'mirror'
        # An instance is either the API or a mirror of the API
        # 
        # A class must be able to query whether it is of 
        # API or API-mirror type
        #
        @tblink.iftype(name="my_api")
        class rv_bfm(object):
            
            def __init__(self):
                self.send_f = None
                self._rsp_f = None
                self._req_f = None
                pass
            
            @tblink.impfunc
            def _req(self, 
                             addr : ctypes.c_uint64,
                             data : ctypes.c_uint8):
                print("_req")
                self._req_f(addr, data)
            
            @tblink.expfunc
            def _rsp(self, data : ctypes.c_uint16):
                print("_rsp")
                self._rsp_f(data)
            
        class Tb(Component):
            """Represents the testbench interacting with a BFM"""
            
            def __init__(self, parent=None, name="C1"):
                super().__init__(parent, name)
                self.rsp_ev = tblink.Event()
                
            def build(self):
                print("TB build")
                self.bfm_i = self.mkInst(rv_bfm, "bfm_i")
                
            def connect(self):
                print("TB connect")
                for ifinst in self.endpoint.peerInterfaceInsts():
                    print("  IfInst: %s" % ifinst.name)
                self.bfm_i._rsp_f = self._rsp
                
            def start(self):
                print("TB.start", flush=True)
                tblink.fork(self.run())
#                asyncio.ensure_future(self.run())
                pass
            
            def _rsp(self, data):
                self.rsp_ev.set()
                
            async def run(self):
                print("--> TB.Run")
                self.raise_objection()
                for i in range(20):
                    self.bfm_i._req(1, 2)
                    
                    print("--> wait_rsp")
                    if not self.rsp_ev.is_set():
                        await self.rsp_ev.wait()
                    self.rsp_ev.clear()
                    print("<-- wait_rsp")
                    
                self.drop_objection()
                print("<-- TB.Run")
            
        class Sim(Component):
            
            def __init__(self, parent=None, name="Sim"):
                super().__init__(parent, name)
                self.inst = None
                self.req_ev = tblink.Event()
                
            def build(self):
                print("Sim build")
                # TODO: do we need the ability to specify the
                # implementation class for an interface?
                self.bfm = self.mkMirrorInst(rv_bfm, "bfm_i")
                
            def connect(self):
                print("Sim connect")
                for ifinst in self.endpoint.peerInterfaceInsts():
                    print("  IfInst: %s" % ifinst.name)
                self.bfm._req_f = self._req_f
                
            def _req_f(self, addr, data):
                print("Sim._req_f")
                self.req_ev.set()
                
            def start(self):
                print("Sim.start", flush=True)
                tblink.fork(self.run())
                
            async def run(self):
                print("--> Sim.Run")
                self.raise_objection()
                for i in range(20):
                    print("--> Sim.req_ev.wait %d" % i)
                    if not self.req_ev.is_set():
                        await self.req_ev.wait()
                    print("<-- Sim.req_ev.wait %d" % i)
                    
                    self.req_ev.clear()
                    
                    print("--> Sim._rsp %d" % i)
                    self.bfm._rsp(0)
                    print("<-- Sim._rsp %d" % i)
                self.drop_objection()
                print("<-- Sim.Run")
                

        tp = TransportDualFifo()
        
        ep1 = EndpointMsgTransport(tp.ep[0])
        ep2 = EndpointMsgTransport(tp.ep[1])

        tb_i = Tb()
        sim_i = Sim()
        
        r1 = Runner(tb_i, ep1)
        r2 = Runner(sim_i, ep2)
        
#        rt1 = asyncio.ensure_future(r1.run())
#        rt2 = asyncio.ensure_future(r2.run())

        loop = asyncio.get_event_loop()
        
        print("--> Run", flush=True)
        t1 = asyncio.ensure_future(r1.run())
        t2 = asyncio.ensure_future(r2.run())
        
        loop.run_until_complete(
            asyncio.wait(
                [
                    asyncio.gather(t1, t2),
                    asyncio.sleep(2)
                ], return_when=asyncio.FIRST_COMPLETED))
#        loop.run_until_complete(asyncio.gather(t1, t2))
        print("<-- Run", flush=True)
        
        self.assertTrue(t1.done())
        self.assertTrue(t2.done())
        
        print("t1.done: %s ; t2.done: %s" % (str(t1.done()), str(t2.done())))

#        self.assertEqual(host_i.inst.call_counts[4], 10)
#        self.assertEqual(host_i.inst.call_counts[0], 1)        
        
        
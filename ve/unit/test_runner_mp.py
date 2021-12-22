'''
Created on Sep 12, 2021

@author: mballance
'''

import asyncio
import ctypes
import socket

from TblinkTestCase import TblinkTestCase
import multiprocessing as mp
import tblink
from tblink_rpc.impl.iftype_rgy import IftypeRgy
from tblink_rpc.component import Component
from tblink_rpc.runtime.runner import Runner
from tblink_rpc_core.endpoint_msg_transport import EndpointMsgTransport
from tblink_rpc_core.transport_json_socket import TransportJsonSocket
from test_endpoint_services import TestEndpointServices


class TestRunnerMP(TblinkTestCase):
    
    def test_smoke(self):
        
        TOTAL_COUNT = 10000
        
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
#                print("_req")
                self._req_f(addr, data)

            # TODO: Consider non-blocking functions
            # maybe streaming/async/...            
            @tblink.expfunc
            def _rsp(self, data : ctypes.c_uint16):
#                print("_rsp")
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
                for i in range(TOTAL_COUNT):
                    self.bfm_i._req(1, 2)
                    
                    if not self.rsp_ev.is_set():
                        await self.rsp_ev.wait()
                    self.rsp_ev.clear()
                    
                self.drop_objection()
                print("<-- TB.Run")                         
        
        def client(port):
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.connect(('localhost', port))
            
            tp = TransportJsonSocket(s)
            ep = EndpointMsgTransport(tp)
            
            ep.init(TestEndpointServices([]), None)
            
            tb_i = Tb()
            r = Runner(tb_i, ep)
            
            loop = asyncio.get_event_loop()
            
            print("--> Tb.Run", flush=True)
            
            t = asyncio.ensure_future(r.run())
   
            loop.run_until_complete(
                asyncio.wait(
                    [
                        t,
                        asyncio.sleep(2)
                    ], return_when=asyncio.FIRST_COMPLETED))
            print("<-- Tb.Run", flush=True)
            print("Tb.done: %s" % str(t.done()))


        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        port = s.getsockname()[1]
            
        s.listen()
        
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
                self.req_ev.set()
                
            def start(self):
                print("Sim.start", flush=True)
                tblink.fork(self.run())
                
            async def run(self):
                print("--> Sim.Run")
                self.raise_objection()
                for i in range(TOTAL_COUNT):
                    if not self.req_ev.is_set():
                        await self.req_ev.wait()
                    
                    self.req_ev.clear()
                    
                    self.bfm._rsp(0)
                self.drop_objection()
                print("<-- Sim.Run")
                                 
        p = mp.Process(target=client, args=(port,))
        p.start()
        
        conn, addr = s.accept()
        conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        t = TransportJsonSocket(conn)        
        ep = EndpointMsgTransport(t)
        sim_i = Sim()
        
        ep.init(TestEndpointServices([]), None)
        
        r = Runner(sim_i, ep)
        
        loop = asyncio.get_event_loop()
        t = asyncio.ensure_future(r.run())

        print("--> Sim.run")
        loop.run_until_complete(
            asyncio.wait(
                [
                    t,
                    asyncio.sleep(2)
                ], return_when=asyncio.FIRST_COMPLETED)) 
        print("<-- Sim.run")
        p.join(1)
        
        if p.is_alive():
            self.fail("process still running")
            p.terminate()
        
        self.assertTrue(t.done())
        
        print("Server: %d iftypes" % len(IftypeRgy.inst().iftypes))
        
        
        
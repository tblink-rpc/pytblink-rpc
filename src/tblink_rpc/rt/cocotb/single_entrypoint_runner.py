
class RegressionManager(object):
    
    _entry = None
    
    def __init__(self, dut, tests):
        print("__init__")
        self._dut = dut
        self._ev = None
        
    def execute(self):
        import cocotb
        print("TODO: execute")
        test_c = cocotb.decorators.test()
#            RegressionManager._entry)
        test_cc = test_c(self.entry)
        test_init_outcome = cocotb.outcomes.capture(
            test_cc,
            self._dut)
        
        test = test_init_outcome.get()
        
        print("test_c=%s" % str(test_c))
        print("test_cc=%s" % str(test_cc))
        print("test_init_outcome=%s" % str(test_init_outcome))
        print("test=%s" % str(test))
        
        cocotb.scheduler._add_test(test)
        
    def event(self, ev):
        print("--> Event")
        print("<-- Event")
        
        
    async def entry(self, dut):
        print("RegressionManager::entry", flush=True)
        from tblink_rpc import cocotb_compat
        import cocotb
        # Run the cocotb init sequence
        ep = await cocotb_compat.init()
        
        # Doesn't really seem to matter if we keep the
        # 'test' running or not.
#        ep.addListener(self.event)
#        self._ev = cocotb.triggers.Event()
        
#        while True:
#            print("--> Wait")
#            await self._ev.wait()
#            print("<-- Wait")
        
        

    @classmethod
    def from_discovery(cls, dut):
        print("from_discovery")
        return RegressionManager(dut, [])

import cocotb
from tblink_rpc import cocotb_compat


async def entry(dut):
    print("--> single_inst_runner::entry", flush=True)
    await cocotb_compat.init()
    print("<-- single_inst_runner::entry", flush=True)
#    await cocotb.triggers.Timer(10, 'us')
    
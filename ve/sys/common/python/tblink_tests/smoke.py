'''
Created on Mar 7, 2021

@author: mballance
'''

#import cocotb
import tblink
import tblink.impl.cocotb as cocotb
from tblink import TimeUnit

@cocotb.test
async def entry(dut):
    print("Test Entry")
    try:
        print("Simtime: " + str(tblink.simtime()))
    except Exception as e:
        print("Exception: " + str(e))

    for i in range(10):
        print("--> Sleep " + str(tblink.simtime()))
        await tblink.sleep(10, "ns")
        print("<-- Sleep " + str(tblink.simtime()))

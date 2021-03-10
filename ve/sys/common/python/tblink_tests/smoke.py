'''
Created on Mar 7, 2021

@author: mballance
'''

#import cocotb
import tblink.impl.cocotb as cocotb

@cocotb.test
async def entry(dut):
    print("Test Entry")

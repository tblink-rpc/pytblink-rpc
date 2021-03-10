'''
Created on Mar 9, 2021

@author: mballance
'''
import asyncio

import tblink
import tblink.impl.cocotb as cocotb
from tblink_test import TblinkTest


class TestSmoke(TblinkTest):
    
    def test_entry(self):
        
        test_func_called = False
        
        @cocotb.test
        async def test_func(dut):
            print("test_func")
            nonlocal test_func_called
            test_func_called = True
            
        self.runTest()
        self.assertTrue(test_func_called)

    def test_fork(self):
        
        task_called = False
        
        async def task():
            nonlocal task_called
            print("test_func")
            task_called = True
            
        @cocotb.test
        async def test_func(dut):
            print("test_func")
            t = tblink.fork(task())
            
            await t
            
        self.runTest()
        self.assertTrue(task_called)

    def test_fork_2(self):
        
        task_called = 0
        
        async def task():
            nonlocal task_called
            print("test_func")
            task_called += 1
            
        @tblink.test()
        async def test_func(dut):
            print("test_func")
            t1 = tblink.fork(task())
            t2 = tblink.fork(task())
            
            await asyncio.gather(t1, t2)
            
        self.runTest()
        self.assertTrue(task_called)

    def test_sleep_1(self):
        
        loop_count = 0
        
        @cocotb.test
        async def test_func(dut):
            nonlocal loop_count
            print("test_func")
            for i in range(10):
                print("--> sleep " + str(tblink.simtime()))
                await tblink.sleep(1)
                print("<-- sleep " + str(tblink.simtime()))
                loop_count += 1
            
        self.runTest()
        self.assertEquals(loop_count, 10)
        self.assertEquals(tblink.simtime(), 10)


                    
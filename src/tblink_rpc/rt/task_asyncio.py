'''
Created on Dec 27, 2021

@author: mballance
'''
from tblink_rpc.task import Task

class TaskAsyncio(Task):
    
    def __init__(self, task):
        self.task = task
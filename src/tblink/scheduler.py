'''
Created on Mar 7, 2021

@author: mballance
'''
from tblink.backend import Backend

class Scheduler(object):
    
    def __init__(self, backend : Backend):
        self.backend = backend
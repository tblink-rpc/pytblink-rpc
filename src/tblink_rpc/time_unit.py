'''
Created on Dec 28, 2021

@author: mballance
'''
from enum import IntEnum

class TimeUnit(IntEnum):
    ps = -12
    ns = -9
    us = -6
    ms = -3
    s = 0
    
    @classmethod
    def str2unit(cls, unit_s):
        if unit_s == "ps":
            return cls.ps
        elif unit_s == "ns":
            return cls.ns
        elif unit_s == "us":
            return cls.us
        elif unit_s == "ms":
            return cls.ms
        elif unit_s == "s":
            return cls.s
        else:
            raise Exception("Unknown type unit \"%s\"" % unit_s)

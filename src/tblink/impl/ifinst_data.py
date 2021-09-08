'''
Created on Sep 7, 2021

@author: mballance
'''

class IfInstData(object):
    
    def __init__(self, ep, ifinst, is_mirror):
        self.ep = ep
        self.ifinst = ifinst
        self.is_mirror = is_mirror
        self.methodt2decl_m = {}


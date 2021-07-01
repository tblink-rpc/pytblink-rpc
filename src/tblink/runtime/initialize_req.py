'''
Created on Mar 31, 2021

@author: mballance
'''
import json

class InitializeReq(object):
    
    def __init__(self):
        pass
    
    def dump(self):
        msg = {
            "method" : "initialize-req",
            "id": 1
        }
        
        return json.dumps(msg)
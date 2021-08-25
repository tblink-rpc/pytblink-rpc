'''
Created on Aug 24, 2021

@author: mballance
'''

class MethodType(object):
    
    def __init__(self, 
                 name, 
                 id,
                 rtype,
                 params,
                 is_task, 
                 is_import):
        self.name = name
        self.id = id
        self.rtype = rtype
        self.params = params
        self.is_task = is_task
        self.is_import = is_import
    
    
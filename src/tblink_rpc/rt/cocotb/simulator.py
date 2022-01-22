'''
Created on Jan 21, 2022

@author: mballance
'''

MODULE = 0
STRUCTURE = 1
REG = 2
NET = 3
NETARRAY = 4
REAL = 5
INTEGER = 6
ENUM = 8
STRING = 9
GENARRAY = 10


class DummyHandle(object):

    def get_const(self):
        return True
    
    def get_type(self):
        return MODULE
    
    def get_name_string(self):
        return ""
    
    def get_type_string(self):
        return "MODULE"
    
    def get_definition_name(self):
        return ""
    
    def get_definition_file(self): 
        return ""
    
    pass

print("tblink_rpc.simulator", flush=True)

def get_root_handle(root_name):
    print("get_root_handle: %s" % str(root_name))
    return DummyHandle()

def register_timed_callback(t, cb, ud):
    print("register_timed_callback")
    
    return []
    pass
    
def log_level(level):
    print("log_level", flush=True)
    pass

def get_sim_time():
    return (0,0)

def get_precision():
    return -9

def get_simulator_product():
    return "TbLink-RPC "

def get_simulator_version():
    return "0.0"

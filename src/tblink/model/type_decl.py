'''
Created on Aug 24, 2021

@author: mballance
'''
from enum import Enum, auto

class TypeDeclE(Enum):
    i8  = auto()
    i16 = auto()
    i32 = auto()
    i64 = auto()
    u8  = auto()
    u16 = auto()
    u32 = auto()
    u64 = auto()
    str = auto()
    vec = auto()
    map = auto()

class TypeDecl(object):
    
    def __init__(self, 
                 base_t : TypeDeclE,
                 key_t : 'TypeDecl' = None,
                 elem_t : 'TypeDecl' = None):
        self.base_t : TypeDeclE = base_t
        # Points to the element type (if relevant)
        self.elem_t = elem_t
        # Points to the key type (if relevant)
        self.key_t = key_t
        
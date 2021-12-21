'''
Created on Sep 6, 2021

@author: mballance
'''
from tblink.impl.type_decl import TypeDecl, TypeDeclE
from tblink_rpc_core.type import Type

class ParamTypeBuilder(object):
    
    def __init__(self, iftype_b):
        self.iftype_b = iftype_b
        
    _width_m = {
        TypeDeclE.i8 : 8,
        TypeDeclE.u8 : 8,
        TypeDeclE.i16 : 16,
        TypeDeclE.u16 : 16,
        TypeDeclE.i32 : 32,
        TypeDeclE.u32 : 32,
        TypeDeclE.i64 : 64,
        TypeDeclE.u64 : 64
    }
    
    _signed_s = {
        TypeDeclE.i8,
        TypeDeclE.i16,
        TypeDeclE.i32,
        TypeDeclE.i64
    }
    
    def build(self, td : TypeDecl) -> Type:
        if td is None:
            return None
        
        if (td.base_t in ParamTypeBuilder._width_m.keys()):
            return self.iftype_b.mkTypeInt(
                td.base_t in ParamTypeBuilder._signed_s,
                ParamTypeBuilder._width_m[td.base_t])
        elif td.base_t == TypeDeclE.bool:
            return self.iftype_b.mkTypeBool()
        elif td.base_t == TypeDeclE.str:
            return self.iftype_b.mkTypeStr()
        elif td.base_t == TypeDeclE.vec:
            return self.iftype_b.mkTypeVec(self.build(td.elem_t))
        elif td.base_t == TypeDeclE.map:
            return self.iftype_b.mkTypeMap(
                self.build(td.key_t),
                self.build(td.elem_t))
            
        pass
    
        
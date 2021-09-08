'''
Created on Jan 31, 2021

@author: mballance
'''
import ctypes
from typing import Dict, List
import typing
from tblink.impl.iftype_rgy import IftypeRgy
from tblink.impl.methodtype_decl import MethodTypeDecl
from tblink.impl.type_decl import TypeDecl, TypeDeclE
from tblink.impl.iftype_decl import IftypeDecl

class Ctor(object):

    _inst = None
    _primitive_types = {
        ctypes.c_ubyte : TypeDeclE.u8,
        ctypes.c_ushort : TypeDeclE.u16,
        ctypes.c_uint : TypeDeclE.u32,
        ctypes.c_ulong : TypeDeclE.u64,
        ctypes.c_byte : TypeDeclE.i8,
        ctypes.c_short : TypeDeclE.i16,
        ctypes.c_int : TypeDeclE.i32,
        ctypes.c_long : TypeDeclE.i64,
        str : TypeDeclE.str
        }
    _supported_types = set()
    
    def __init__(self):
        # Methods collected to be 
        self.methods = []
        self.method_m = {}
    
    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = Ctor()
        return cls._inst
    
    @classmethod
    def reset(cls):
        cls._inst = None
        
    def add_method(
            self,
            T,
            is_export,
            is_task):
        fi = T.__code__

        rtype = None
        params = []        
        if fi.co_argcount > 0:
            if hasattr(T, "__annotations__"):
#                if is_task and "return" in T.__annotations__.keys():
#                    raise Exception("Cannot specify a return type for a task")
#                elif not is_task and hasattr(T.__annotations__, "return"):
                if not is_task and hasattr(T.__annotations__, "return"):
                    rtype = T.__annotations__["return"]
                    
                for pname in fi.co_varnames[1:fi.co_argcount]:
                    if pname in T.__annotations__.keys():
                        ptype = T.__annotations__[pname]
                        # TODO: validate type
                        ptype_o = self._build_tdecl(ptype)
                        
                        pdecl = (pname, ptype_o)
                        
                        # TODO: need to get default value?
                        
                        params.append(pdecl)
                    else:
                        raise Exception("Type for parameter " + pname + " unspecified")
            else:
                raise Exception("No annotations")
            
        rtype_o = None if rtype is None else self._build_tdecl(rtype)

        if T.__name__ in self.method_m.keys():
            raise Exception("Error: duplicate method name %s", T.__name__)
            
        m = MethodTypeDecl(
            T.__name__,
            len(self.methods),
            rtype_o,
            params,
            is_export,
            is_task)
        self.methods.append(m)
        self.method_m[T.__name__] = m
        return m
    
    def _build_tdecl(self, ptype):
        ret = None
        if ptype in Ctor._primitive_types.keys():
            base_t = Ctor._primitive_types[ptype]
            print("type: %s" % str(base_t))
            ret = TypeDecl(base_t)
        elif isinstance(ptype, Dict):
            base_t = TypeDeclE.map
        elif isinstance(ptype, List):
            print("ptype: %s %s" % (str(ptype), str(type(ptype))))
        elif isinstance(ptype, typing.List):
            print("list(1)")
        elif ptype == typing.List:
            print("list:")
        elif ptype is typing.List:
            print("list(2):")
        elif type(ptype) == typing.List:
            print("list(3):")
        elif isinstance(ptype, typing.GenericMeta):
            base_t = None
            elem_t = None
            key_t = None
            if ptype.__origin__ == typing.List:
                base_t = TypeDeclE.vec
                elem_t = self._build_tdecl(ptype.__args__[0])
            elif ptype.__origin__ == typing.Dict:
                base_t = TypeDeclE.map
                key_t = self._build_tdecl(ptype.__args__[0])
                elem_t = self._build_tdecl(ptype.__args__[1])
            else:
                raise Exception("Unsupported type annotation %s" % str(ptype))
                
                
            ret = TypeDecl(base_t, key_t, elem_t)

        elif ptype == int:
            raise Exception("Python 'int' cannot be used as a type. use ctypes.c_int instead")                
        else:
            print("unhandled")
        print("base_t: %s" % str(base_t))
        print("ptype: %s %s" % (str(ptype), str(type(ptype))))
        
        return ret
        
    
    def add_iftype(self, T, name):
        print("add_iftype: %s" % name)
        iftype = IftypeDecl(
            name,
            T,
            self.methods.copy())
        self.methods.clear()
        self.method_m.clear()

        IftypeRgy.inst().add_iftype(iftype)
        
    def add_bundle(self, T):
        if hasattr(T, "__annotations__"):
            for key in T.__annotations__.keys():
                pass
#             if is_task and "return" in T.__annotations__.keys():
#                 raise Exception("Cannot specify a return type for a task")
#             elif not is_task and hasattr(T.__annotations__, "return"):
#                 rtype = T.__annotations__["return"]
#                     
#             for pname in fi.co_varnames[1:fi.co_argcount]:
#                 if pname in T.__annotations__.keys():
#                     ptype = T.__annotations__[pname]
#                     # TODO: validate type
#                     print("pname: " + pname + " " + str(ptype))
#                     params.append(ParamDef(pname, ptype))
#                 else:
#                     raise Exception("Type for parameter " + pname + " unspecified")
        else:
            raise Exception("No annotations")        
        pass
    
    
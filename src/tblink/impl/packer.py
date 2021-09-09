'''
Created on Sep 9, 2021

@author: mballance
'''
from tblink.impl.type_decl import TypeDecl
from tblink_rpc_core.type_e import TypeE
from tblink_rpc_core.type import Type

class Packer(object):
    
    def __init__(self, ep):
        self.ep = ep
        pass
    
    def pack_value(self, val, type : Type):
        ret = None
        
        if type.kind() == TypeE.Int:
            width = 32 # TODO
            is_signed = True # TODO
            
            ret = self.ep.mkValIntS(int(val), width)
        elif type.kind() == TypeE.Bool:
            ret = self.ep.mkValBool(bool(val))
        elif type.kind() == TypeE.Str:
            ret = self.ep.mkValStr(str(val))
        elif type.kind() == TypeE.Vec:
            ret = self.ep.mkValVec()
            
            for e in val:
                ret.push_back(self.pack_value(e, type.elem_t()))
        elif type.kind() == TypeE.Map:
            ret = self.ep.mkValMap()
            
            for k in val.keys():
                key_v = self.pack_value(k, type.key_t())
                ret.setVal(key_v, self.pack_value(
                    val[k],
                    type.elem_t()))
        else:
            raise Exception("Unimplemented param type %s" % str(type.kind()))

        return ret                    
    
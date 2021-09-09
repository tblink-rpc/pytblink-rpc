'''
Created on Sep 9, 2021

@author: mballance
'''
from tblink_rpc_core.param_val import ParamVal
from tblink_rpc_core.type import Type
from tblink_rpc_core.type_e import TypeE

class Unpacker(object):
    
    def __init__(self):
        pass
    
    def unpack_val(self, val : ParamVal, type : Type):

        ret = None        
        
        if type.kind() == TypeE.Int:
            ret = val.val_s()
        elif type.kind() == TypeE.Bool:
            ret = val.val()
        elif type.kind() == TypeE.Str:
            ret = val.val()
        elif type.kind() == TypeE.Vec:
            ret = []
            for i in range(val.size()):
                ret.append(self.unpack_vak(val.at(i), type.elem_t()))
        elif type.kind() == TypeE.Map:
            ret = {}
            
            for k in val.getKeys():
                k_v = self.unpack_val(k, val.key_t())
                ret[k_v] = self.unpack_val(val.getVal(k), val.elem_t())
        else:
            raise Exception("Unsupported type %s" % str(type.kind()))
        
        return ret

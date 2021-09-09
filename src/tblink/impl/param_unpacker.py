'''
Created on Sep 8, 2021

@author: mballance
'''
from typing import List

from tblink_rpc_core.method_type import MethodType
from tblink_rpc_core.param_val_vec import ParamValVec
from tblink_rpc_core.type_e import TypeE


class ParamUnpacker(object):
    
    def __init__(self):
        pass
    
    def unpack(self, 
               method_t : MethodType, 
               params : ParamValVec) -> List:
        ret = []
        
        for i,pt in enumerate(method_t.params()):
            if pt.type().kind() == TypeE.Int:
                width = 32 # TODO
                is_signed = True # TODO

                ret.append(params.at(i).val_s())                
            elif pt.type().kind() == TypeE.Bool:
                ret.append(params.at(i).val())
            elif pt.type().kind() == TypeE.Str:
                ret.append(params.at(i).val())
            else:
                raise Exception("Unimplemented param type %s" % str(pt.type()))        
        
        return ret
    
'''
Created on Sep 5, 2021

@author: mballance
'''
from tblink_rpc_core.param_val_vec import ParamValVec
from tblink_rpc_core.type_e import TypeE

class ParamPacker(object):
    
    def __init__(self, ep, method_t):
        self.ep = ep
        self.method_t = method_t
        
    def pack(self, *args, **kwargs) -> ParamValVec:
        if len(kwargs) > 0:
            raise Exception("Specifying kwargs is not supported")
        
        ret = self.ep.mkValVec()
        
        for i,pt in enumerate(self.method_t.params()):
            if pt.type().kind() == TypeE.Int:
                width = 32 # TODO
                is_signed = True # TODO
                
                ret.push_back(self.ep.mkValIntS(args[i], width))
            elif pt.type().kind() == TypeE.Bool:
                ret.push_back(self.ep.mkValBool(bool(args[i])))
            elif pt.type().kind() == TypeE.Str:
                ret.push_back(self.ep.mkValStr(str(args[i])))
            else:
                raise Exception("Unimplemented param type %s" % str(pt.type()))
            
        return ret
    
# distutils: language = c++
#****************************************************************************
#* tblink_core.pyx
#*
#****************************************************************************
#from tblink.backend import Backend

# Import the map and vector templates from the STL
from libcpp.string cimport string as cpp_string
from libcpp.map cimport map as cpp_map
from libcpp.vector cimport vector as cpp_vector
from libcpp.utility cimport pair as cpp_pair
from libcpp cimport bool as bool
from tblink.tblink import TbLink

ctypedef unsigned long long   uint64_t
ctypedef long long            int64_t
ctypedef unsigned int         uint32_t

cdef extern from "IBackend.h" namespace "tblink":

    ctypedef void (*cb_f)(void *)
    ctypedef bool (*reschedule_f)()

    cdef cppclass IBackend:
    
        void init(reschedule_f)
        
        uint64_t simtime()
        
        uint64_t add_simtime_cb(
            uint64_t        delta,
            cb_f            cb,
            void            *ud)
        
        void remove_simtime_cb(
            uint64_t        id)
       

cdef void _cb_closure(void *ud):
    print("--> _cb_closure")
    (<object>ud)()
    print("<-- _cb_closure")
    
cdef bool _reschedule():
    print("--> _reschedule")
    ret = TbLink.inst().reschedule()
    print("<-- _reschedule")
    return ret

cdef class BackendNative(object):
    cdef IBackend      *backend
    
    def __init__(self, uint64_t backend):
        # We pass the pointer as a uint for convenience
        self.backend = <IBackend *>backend
        self.backend.init(_reschedule)
        
    def simtime(self):
        return self.backend.simtime()
    
    def add_simtime_cb(self, delta : int, cb) -> int:
        print("-- add_simtime_cb " + str(delta) + " " + str(cb))
        return self.backend.add_simtime_cb(delta, _cb_closure, <void*>cb)
        
    def remove_simtime_cb(self, id):
        self.backend.remove_simtime_cb(id)
        

# Need to know about IBackend 
print("Hello: tblink_core.pyx")



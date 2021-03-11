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

ctypedef unsigned long long   uint64_t
ctypedef long long            int64_t
ctypedef unsigned int         uint32_t

cdef extern from "IBackend.h" namespace "tblink":

    cdef cppclass IBackend:
        uint64_t simtime()


cdef class BackendNative(object):
    cdef IBackend      *backend
    
    def __init__(self, uint64_t backend):
        # We pass the pointer as a uint for convenience
        self.backend = <IBackend *>backend
        
    def simtime(self):
        return self.backend.simtime()
        

# Need to know about IBackend 
print("Hello: tblink_core.pyx")



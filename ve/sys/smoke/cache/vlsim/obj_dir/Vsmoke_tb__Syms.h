// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef _VSMOKE_TB__SYMS_H_
#define _VSMOKE_TB__SYMS_H_  // guard

#include "verilated_heavy.h"

// INCLUDE MODULE CLASSES
#include "Vsmoke_tb.h"
#include "Vsmoke_tb_tblink_pkg.h"

// DPI TYPES for DPI Export callbacks (Internal use)

// SYMS CLASS
class Vsmoke_tb__Syms : public VerilatedSyms {
  public:
    
    // LOCAL STATE
    const char* __Vm_namep;
    bool __Vm_didInit;
    
    // SUBCELL STATE
    Vsmoke_tb*                     TOPp;
    Vsmoke_tb_tblink_pkg           TOP__tblink_pkg;
    
    // SCOPE NAMES
    VerilatedScope __Vscope_tblink_pkg;
    
    // SCOPE HIERARCHY
    VerilatedHierarchy __Vhier;
    
    // CREATORS
    Vsmoke_tb__Syms(Vsmoke_tb* topp, const char* namep);
    ~Vsmoke_tb__Syms() {}
    
    // METHODS
    inline const char* name() { return __Vm_namep; }
    
} VL_ATTR_ALIGNED(VL_CACHE_LINE_BYTES);

#endif  // guard

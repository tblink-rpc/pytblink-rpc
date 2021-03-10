// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vvltest.h for the primary calling header

#ifndef _VVLTEST_CLS_PKG_H_
#define _VVLTEST_CLS_PKG_H_  // guard

#include "verilated_heavy.h"

//==========

class Vvltest__Syms;

//----------

VL_MODULE(Vvltest_cls_pkg) {
  public:
    
    // INTERNAL VARIABLES
  private:
    Vvltest__Syms* __VlSymsp;  // Symbol table
  public:
    
    // CONSTRUCTORS
  private:
    VL_UNCOPYABLE(Vvltest_cls_pkg);  ///< Copying not allowed
  public:
    Vvltest_cls_pkg(const char* name = "TOP");
    ~Vvltest_cls_pkg();
    
    // INTERNAL METHODS
    void __Vconfigure(Vvltest__Syms* symsp, bool first);
  private:
    void _ctor_var_reset() VL_ATTR_COLD;
} VL_ATTR_ALIGNED(VL_CACHE_LINE_BYTES);

//----------


#endif  // guard

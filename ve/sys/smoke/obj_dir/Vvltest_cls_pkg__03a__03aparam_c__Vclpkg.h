// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vvltest.h for the primary calling header

#ifndef _VVLTEST_CLS_PKG__03A__03APARAM_C__VCLPKG_H_
#define _VVLTEST_CLS_PKG__03A__03APARAM_C__VCLPKG_H_  // guard

#include "verilated_heavy.h"

//==========

class Vvltest__Syms;

//----------

VL_MODULE(Vvltest_cls_pkg__03a__03aparam_c__Vclpkg) {
  public:
    
    // INTERNAL VARIABLES
  private:
    Vvltest__Syms* __VlSymsp;  // Symbol table
  public:
    
    // CONSTRUCTORS
  private:
    VL_UNCOPYABLE(Vvltest_cls_pkg__03a__03aparam_c__Vclpkg);  ///< Copying not allowed
  public:
    Vvltest_cls_pkg__03a__03aparam_c__Vclpkg(const char* name = "TOP");
    ~Vvltest_cls_pkg__03a__03aparam_c__Vclpkg();
    
    // INTERNAL METHODS
    void __Vconfigure(Vvltest__Syms* symsp, bool first);
  private:
    void _ctor_var_reset() VL_ATTR_COLD;
} VL_ATTR_ALIGNED(VL_CACHE_LINE_BYTES);

//----------


//==========

class Vvltest__Syms;

//----------

class Vvltest_cls_pkg__03a__03aparam_c {
  public:
    
    // INTERNAL VARIABLES
    
    // INTERNAL METHODS
  private:
    void _ctor_var_reset(Vvltest__Syms* __restrict vlSymsp);
  public:
    Vvltest_cls_pkg__03a__03aparam_c(Vvltest__Syms* __restrict vlSymsp);
    std::string to_string() const;
    std::string to_string_middle() const;
    ~Vvltest_cls_pkg__03a__03aparam_c();
};

//----------

std::string VL_TO_STRING(const VlClassRef<Vvltest_cls_pkg__03a__03aparam_c>& obj);

#endif  // guard

// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vvltest.h for the primary calling header

#ifndef _VVLTEST_CLS_PKG__03A__03ALIST_C__VCLPKG_H_
#define _VVLTEST_CLS_PKG__03A__03ALIST_C__VCLPKG_H_  // guard

#include "verilated_heavy.h"

//==========

class Vvltest__Syms;

//----------

VL_MODULE(Vvltest_cls_pkg__03a__03alist_c__Vclpkg) {
  public:
    
    // INTERNAL VARIABLES
  private:
    Vvltest__Syms* __VlSymsp;  // Symbol table
  public:
    
    // CONSTRUCTORS
  private:
    VL_UNCOPYABLE(Vvltest_cls_pkg__03a__03alist_c__Vclpkg);  ///< Copying not allowed
  public:
    Vvltest_cls_pkg__03a__03alist_c__Vclpkg(const char* name = "TOP");
    ~Vvltest_cls_pkg__03a__03alist_c__Vclpkg();
    
    // INTERNAL METHODS
    void __Vconfigure(Vvltest__Syms* symsp, bool first);
  private:
    void _ctor_var_reset() VL_ATTR_COLD;
} VL_ATTR_ALIGNED(VL_CACHE_LINE_BYTES);

//----------


//==========

class Vvltest__Syms;
class Vvltest_cls_pkg__03a__03apyval_c;
class Vvltest_cls_pkg__03a__03alist_c;


//----------

class Vvltest_cls_pkg__03a__03alist_c {
  public:
    
    // LOCAL SIGNALS
    VlQueue<VlClassRef<Vvltest_cls_pkg__03a__03apyval_c>> __PVT__elems;
    
    // INTERNAL VARIABLES
    
    // INTERNAL METHODS
    void __VnoInFunc_add_i(Vvltest__Syms* __restrict vlSymsp, IData/*31:0*/ v);
    void __VnoInFunc_add_s(Vvltest__Syms* __restrict vlSymsp, IData/*31:0*/ v);
    void __VnoInFunc_i(Vvltest__Syms* __restrict vlSymsp, IData/*31:0*/ v, VlClassRef<Vvltest_cls_pkg__03a__03alist_c> (&i__Vfuncrtn));
    void __VnoInFunc_s(Vvltest__Syms* __restrict vlSymsp, std::string v, VlClassRef<Vvltest_cls_pkg__03a__03alist_c> (&s__Vfuncrtn));
  private:
    void _ctor_var_reset(Vvltest__Syms* __restrict vlSymsp);
  public:
    Vvltest_cls_pkg__03a__03alist_c(Vvltest__Syms* __restrict vlSymsp);
    std::string to_string() const;
    std::string to_string_middle() const;
    ~Vvltest_cls_pkg__03a__03alist_c();
};

//----------

std::string VL_TO_STRING(const VlClassRef<Vvltest_cls_pkg__03a__03alist_c>& obj);

#endif  // guard

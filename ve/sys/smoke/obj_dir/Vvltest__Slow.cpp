// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vvltest.h for the primary calling header

#include "Vvltest.h"
#include "Vvltest__Syms.h"
#include "Vvltest_cls_pkg__03a__03alist_c__Vclpkg.h"
#include "Vvltest_cls_pkg__03a__03apyval_c__Vclpkg.h"


//==========

Vvltest::Vvltest(const char* __VCname)
    : VerilatedModule(__VCname)
 {
    Vvltest__Syms* __restrict vlSymsp = __VlSymsp = new Vvltest__Syms(this, name());
    Vvltest* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    VL_CELL(__PVT__cls_pkg, Vvltest_cls_pkg);
    VL_CELL(cls_pkg__03a__03apyval_c__Vclpkg, Vvltest_cls_pkg__03a__03apyval_c__Vclpkg);
    VL_CELL(cls_pkg__03a__03aparam_c__Vclpkg, Vvltest_cls_pkg__03a__03aparam_c__Vclpkg);
    VL_CELL(cls_pkg__03a__03alist_c__Vclpkg, Vvltest_cls_pkg__03a__03alist_c__Vclpkg);
    // Reset internal values
    
    // Reset structure values
    _ctor_var_reset();
}

void Vvltest::__Vconfigure(Vvltest__Syms* vlSymsp, bool first) {
    if (false && first) {}  // Prevent unused
    this->__VlSymsp = vlSymsp;
    if (false && this->__VlSymsp) {}  // Prevent unused
    Verilated::timeunit(-12);
    Verilated::timeprecision(-12);
}

Vvltest::~Vvltest() {
    VL_DO_CLEAR(delete __VlSymsp, __VlSymsp = nullptr);
}

void Vvltest::_initial__TOP__1(Vvltest__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vvltest::_initial__TOP__1\n"); );
    Vvltest* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Variables
    VlClassRef<Vvltest_cls_pkg__03a__03alist_c> __Vfunc_list__0__Vfuncout;
    VlClassRef<Vvltest_cls_pkg__03a__03alist_c> __Vfunc_list__0__ret;
    // Body
    VL_WRITEF("Hello\n");
    __Vfunc_list__0__ret = std::make_shared<Vvltest_cls_pkg__03a__03alist_c>(vlSymsp);
    __Vfunc_list__0__Vfuncout = __Vfunc_list__0__ret;
    vlTOPp->top__DOT__unnamedblk1__DOT__l = __Vfunc_list__0__Vfuncout;
    VL_NULL_CHECK(vlTOPp->top__DOT__unnamedblk1__DOT__l, "vltest.sv", 70)->__VnoInFunc_add_i(vlSymsp, 5U);
    VL_NULL_CHECK(vlTOPp->top__DOT__unnamedblk1__DOT__l, "vltest.sv", 71)->__VnoInFunc_add_s(vlSymsp, 0x626f6fU);
    VL_NULL_CHECK(vlTOPp->top__DOT__unnamedblk1__DOT__l, "vltest.sv", 72)->__VnoInFunc_add_i(vlSymsp, 0x3230U);
}

void Vvltest::_eval_initial(Vvltest__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vvltest::_eval_initial\n"); );
    Vvltest* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->_initial__TOP__1(vlSymsp);
}

void Vvltest::final() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vvltest::final\n"); );
    // Variables
    Vvltest__Syms* __restrict vlSymsp = this->__VlSymsp;
    Vvltest* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
}

void Vvltest::_eval_settle(Vvltest__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vvltest::_eval_settle\n"); );
    Vvltest* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
}

void Vvltest::_ctor_var_reset() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vvltest::_ctor_var_reset\n"); );
    // Body
    clock = VL_RAND_RESET_I(1);
    }

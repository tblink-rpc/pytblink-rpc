// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vvltest.h for the primary calling header

#include "Vvltest_cls_pkg__03a__03alist_c__Vclpkg.h"
#include "Vvltest__Syms.h"

//==========

//==========

Vvltest_cls_pkg__03a__03alist_c::Vvltest_cls_pkg__03a__03alist_c(Vvltest__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+  Vvltest_cls_pkg__03a__03alist_c::new\n"); );
    // Variables
    _ctor_var_reset(vlSymsp);
    Vvltest* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
}

void Vvltest_cls_pkg__03a__03alist_c::__VnoInFunc_add_i(Vvltest__Syms* __restrict vlSymsp, IData/*31:0*/ v) {
    VL_DEBUG_IF(VL_DBG_MSGF("+  Vvltest_cls_pkg__03a__03alist_c::__VnoInFunc_add_i\n"); );
    // Variables
    VlClassRef<Vvltest_cls_pkg__03a__03apyval_c> pv;
    Vvltest* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    pv = std::make_shared<Vvltest_cls_pkg__03a__03apyval_c>(vlSymsp);
    VL_WRITEF("i(%0d)\n",32,v);
    this->__PVT__elems.push_back(pv);
}

void Vvltest_cls_pkg__03a__03alist_c::__VnoInFunc_add_s(Vvltest__Syms* __restrict vlSymsp, IData/*31:0*/ v) {
    VL_DEBUG_IF(VL_DBG_MSGF("+  Vvltest_cls_pkg__03a__03alist_c::__VnoInFunc_add_s\n"); );
    // Variables
    VlClassRef<Vvltest_cls_pkg__03a__03apyval_c> pv;
    Vvltest* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    pv = std::make_shared<Vvltest_cls_pkg__03a__03apyval_c>(vlSymsp);
    VL_WRITEF("s(%0s)\n",32,v);
    this->__PVT__elems.push_back(pv);
}

void Vvltest_cls_pkg__03a__03alist_c::__VnoInFunc_i(Vvltest__Syms* __restrict vlSymsp, IData/*31:0*/ v, VlClassRef<Vvltest_cls_pkg__03a__03alist_c> (&i__Vfuncrtn)) {
    VL_DEBUG_IF(VL_DBG_MSGF("+  Vvltest_cls_pkg__03a__03alist_c::__VnoInFunc_i\n"); );
    // Variables
    Vvltest* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    VL_WRITEF("Error: Verilator doesn't support 'this'\n");
    VL_FINISH_MT("vltest.sv", 34, "");
    i__Vfuncrtn = 0U;
}

void Vvltest_cls_pkg__03a__03alist_c::__VnoInFunc_s(Vvltest__Syms* __restrict vlSymsp, std::string v, VlClassRef<Vvltest_cls_pkg__03a__03alist_c> (&s__Vfuncrtn)) {
    VL_DEBUG_IF(VL_DBG_MSGF("+  Vvltest_cls_pkg__03a__03alist_c::__VnoInFunc_s\n"); );
    // Variables
    Vvltest* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    VL_WRITEF("Error: Verilator doesn't support 'this'\n");
    VL_FINISH_MT("vltest.sv", 45, "");
    s__Vfuncrtn = 0U;
}

void Vvltest_cls_pkg__03a__03alist_c::_ctor_var_reset(Vvltest__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+  Vvltest_cls_pkg__03a__03alist_c::_ctor_var_reset\n"); );
    // Body
    if (false && vlSymsp) {}  // Prevent unused
    }

Vvltest_cls_pkg__03a__03alist_c::~Vvltest_cls_pkg__03a__03alist_c() {
    VL_DEBUG_IF(VL_DBG_MSGF("+  Vvltest_cls_pkg__03a__03alist_c::~\n"); );
}

std::string VL_TO_STRING(const VlClassRef<Vvltest_cls_pkg__03a__03alist_c>& obj) {
    VL_DEBUG_IF(VL_DBG_MSGF("+  Vvltest_cls_pkg__03a__03alist_c::VL_TO_STRING\n"); );
    // Body
    return (obj ? obj->to_string() : "null");
}

std::string Vvltest_cls_pkg__03a__03alist_c::to_string() const {
    VL_DEBUG_IF(VL_DBG_MSGF("+  Vvltest_cls_pkg__03a__03alist_c::to_string\n"); );
    // Body
    return (std::string("'{") + to_string_middle() + "}");
}

std::string Vvltest_cls_pkg__03a__03alist_c::to_string_middle() const {
    VL_DEBUG_IF(VL_DBG_MSGF("+  Vvltest_cls_pkg__03a__03alist_c::to_string_middle\n"); );
    // Body
    std::string out;
    out += "elems:" + VL_TO_STRING(__PVT__elems);
    return out;
}

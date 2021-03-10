// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vvltest.h for the primary calling header

#include "Vvltest_cls_pkg__03a__03apyval_c__Vclpkg.h"
#include "Vvltest__Syms.h"

//==========

//==========

Vvltest_cls_pkg__03a__03apyval_c::Vvltest_cls_pkg__03a__03apyval_c(Vvltest__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+  Vvltest_cls_pkg__03a__03apyval_c::new\n"); );
    // Variables
    _ctor_var_reset(vlSymsp);
    Vvltest* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
}

void Vvltest_cls_pkg__03a__03apyval_c::_ctor_var_reset(Vvltest__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+  Vvltest_cls_pkg__03a__03apyval_c::_ctor_var_reset\n"); );
    // Body
    if (false && vlSymsp) {}  // Prevent unused
}

Vvltest_cls_pkg__03a__03apyval_c::~Vvltest_cls_pkg__03a__03apyval_c() {
    VL_DEBUG_IF(VL_DBG_MSGF("+  Vvltest_cls_pkg__03a__03apyval_c::~\n"); );
}

std::string VL_TO_STRING(const VlClassRef<Vvltest_cls_pkg__03a__03apyval_c>& obj) {
    VL_DEBUG_IF(VL_DBG_MSGF("+  Vvltest_cls_pkg__03a__03apyval_c::VL_TO_STRING\n"); );
    // Body
    return (obj ? obj->to_string() : "null");
}

std::string Vvltest_cls_pkg__03a__03apyval_c::to_string() const {
    VL_DEBUG_IF(VL_DBG_MSGF("+  Vvltest_cls_pkg__03a__03apyval_c::to_string\n"); );
    // Body
    return (std::string("'{") + to_string_middle() + "}");
}

std::string Vvltest_cls_pkg__03a__03apyval_c::to_string_middle() const {
    VL_DEBUG_IF(VL_DBG_MSGF("+  Vvltest_cls_pkg__03a__03apyval_c::to_string_middle\n"); );
    // Body
    std::string out;
    return out;
}

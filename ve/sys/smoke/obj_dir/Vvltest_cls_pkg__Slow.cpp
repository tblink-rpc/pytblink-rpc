// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vvltest.h for the primary calling header

#include "Vvltest_cls_pkg.h"
#include "Vvltest__Syms.h"

//==========

Vvltest_cls_pkg::Vvltest_cls_pkg(const char* __VCname)
    : VerilatedModule(__VCname)
 {
    // Reset internal values
    // Reset structure values
    _ctor_var_reset();
}

void Vvltest_cls_pkg::__Vconfigure(Vvltest__Syms* vlSymsp, bool first) {
    if (false && first) {}  // Prevent unused
    this->__VlSymsp = vlSymsp;
    if (false && this->__VlSymsp) {}  // Prevent unused
}

Vvltest_cls_pkg::~Vvltest_cls_pkg() {
}

void Vvltest_cls_pkg::_ctor_var_reset() {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vvltest_cls_pkg::_ctor_var_reset\n"); );
}

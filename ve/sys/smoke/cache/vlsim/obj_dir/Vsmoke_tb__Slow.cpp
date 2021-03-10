// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsmoke_tb.h for the primary calling header

#include "Vsmoke_tb.h"
#include "Vsmoke_tb__Syms.h"

#include "verilated_dpi.h"

//==========

VL_CTOR_IMP(Vsmoke_tb) {
    Vsmoke_tb__Syms* __restrict vlSymsp = __VlSymsp = new Vsmoke_tb__Syms(this, name());
    Vsmoke_tb* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    VL_CELL(__PVT__tblink_pkg, Vsmoke_tb_tblink_pkg);
    // Reset internal values
    
    // Reset structure values
    _ctor_var_reset();
}

void Vsmoke_tb::__Vconfigure(Vsmoke_tb__Syms* vlSymsp, bool first) {
    if (false && first) {}  // Prevent unused
    this->__VlSymsp = vlSymsp;
    if (false && this->__VlSymsp) {}  // Prevent unused
    Verilated::timeunit(-12);
    Verilated::timeprecision(-12);
}

Vsmoke_tb::~Vsmoke_tb() {
    VL_DO_CLEAR(delete __VlSymsp, __VlSymsp = nullptr);
}

void Vsmoke_tb::_eval_initial(Vsmoke_tb__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsmoke_tb::_eval_initial\n"); );
    Vsmoke_tb* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlSymsp->TOP__tblink_pkg._initial__TOP__tblink_pkg__1(vlSymsp);
}

void Vsmoke_tb::final() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsmoke_tb::final\n"); );
    // Variables
    Vsmoke_tb__Syms* __restrict vlSymsp = this->__VlSymsp;
    Vsmoke_tb* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
}

void Vsmoke_tb::_eval_settle(Vsmoke_tb__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsmoke_tb::_eval_settle\n"); );
    Vsmoke_tb* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
}

void Vsmoke_tb::_ctor_var_reset() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vsmoke_tb::_ctor_var_reset\n"); );
    // Body
    clock = VL_RAND_RESET_I(1);
}

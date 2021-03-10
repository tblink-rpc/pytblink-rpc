// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsmoke_tb.h for the primary calling header

#include "Vsmoke_tb_tblink_pkg.h"
#include "Vsmoke_tb__Syms.h"

#include "verilated_dpi.h"

//==========

VL_CTOR_IMP(Vsmoke_tb_tblink_pkg) {
    // Reset internal values
    // Reset structure values
    _ctor_var_reset();
}

void Vsmoke_tb_tblink_pkg::__Vconfigure(Vsmoke_tb__Syms* vlSymsp, bool first) {
    if (false && first) {}  // Prevent unused
    this->__VlSymsp = vlSymsp;
    if (false && this->__VlSymsp) {}  // Prevent unused
}

Vsmoke_tb_tblink_pkg::~Vsmoke_tb_tblink_pkg() {
}

void Vsmoke_tb_tblink_pkg::_initial__TOP__tblink_pkg__1(Vsmoke_tb__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsmoke_tb_tblink_pkg::_initial__TOP__tblink_pkg__1\n"); );
    Vsmoke_tb* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Variables
    IData/*31:0*/ __Vfunc__init_tblink__0__ret;
    IData/*31:0*/ __Vfunc__tblink_dpi_init__1__Vfuncout;
    QData/*63:0*/ __Vfunc__init_tblink__0__l;
    QData/*63:0*/ __Vfunc__tblink_pylist_new__2__Vfuncout;
    // Body
    vlSymsp->TOP__tblink_pkg.__Vdpiimwrap__tblink_dpi_init_TOP__tblink_pkg(
                                                                           (&(vlSymsp->__Vscope_tblink_pkg)), 
                                                                           "/project/fun/pytblink/pytblink/src/tblink/hvl/tblink_pkg.sv", 0x1bU, 0U, __Vfunc__tblink_dpi_init__1__Vfuncout);
    __Vfunc__init_tblink__0__ret = __Vfunc__tblink_dpi_init__1__Vfuncout;
    vlSymsp->TOP__tblink_pkg.__Vdpiimwrap__tblink_pylist_new_TOP__tblink_pkg(0xaU, __Vfunc__tblink_pylist_new__2__Vfuncout);
    __Vfunc__init_tblink__0__l = __Vfunc__tblink_pylist_new__2__Vfuncout;
    VL_WRITEF("l=%20#\n",64,__Vfunc__init_tblink__0__l);
    if (VL_UNLIKELY((1U != __Vfunc__init_tblink__0__ret))) {
        VL_WRITEF("Error: Failed to initialize PyTblink backend\n");
        VL_FINISH_MT("/project/fun/pytblink/pytblink/src/tblink/hvl/tblink_pkg.sv", 40, "");
    }
}

void Vsmoke_tb_tblink_pkg::_ctor_var_reset() {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsmoke_tb_tblink_pkg::_ctor_var_reset\n"); );
}

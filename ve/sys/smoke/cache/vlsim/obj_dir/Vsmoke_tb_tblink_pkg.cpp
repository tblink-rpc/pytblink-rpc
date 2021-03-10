// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsmoke_tb.h for the primary calling header

#include "Vsmoke_tb_tblink_pkg.h"
#include "Vsmoke_tb__Syms.h"

#include "verilated_dpi.h"

//==========

VL_INLINE_OPT void Vsmoke_tb_tblink_pkg::__Vdpiimwrap__tblink_dpi_init_TOP__tblink_pkg(const VerilatedScope* __Vscopep, const char* __Vfilenamep, IData/*31:0*/ __Vlineno, IData/*31:0*/ have_blocking_tasks, IData/*31:0*/ (&_tblink_dpi_init__Vfuncrtn)) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsmoke_tb_tblink_pkg::__Vdpiimwrap__tblink_dpi_init_TOP__tblink_pkg\n"); );
    // Body
    int have_blocking_tasks__Vcvt;
    have_blocking_tasks__Vcvt = have_blocking_tasks;
    Verilated::dpiContext(__Vscopep, __Vfilenamep, __Vlineno);
    int _tblink_dpi_init__Vfuncrtn__Vcvt;
    _tblink_dpi_init__Vfuncrtn__Vcvt = _tblink_dpi_init(have_blocking_tasks__Vcvt);
    _tblink_dpi_init__Vfuncrtn = _tblink_dpi_init__Vfuncrtn__Vcvt;
}

VL_INLINE_OPT void Vsmoke_tb_tblink_pkg::__Vdpiimwrap__tblink_pylist_new_TOP__tblink_pkg(IData/*31:0*/ sz, QData/*63:0*/ (&_tblink_pylist_new__Vfuncrtn)) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vsmoke_tb_tblink_pkg::__Vdpiimwrap__tblink_pylist_new_TOP__tblink_pkg\n"); );
    // Body
    unsigned int sz__Vcvt;
    sz__Vcvt = sz;
    void* _tblink_pylist_new__Vfuncrtn__Vcvt;
    _tblink_pylist_new__Vfuncrtn__Vcvt = _tblink_pylist_new(sz__Vcvt);
    _tblink_pylist_new__Vfuncrtn = VL_CVT_VP_Q(_tblink_pylist_new__Vfuncrtn__Vcvt);
}

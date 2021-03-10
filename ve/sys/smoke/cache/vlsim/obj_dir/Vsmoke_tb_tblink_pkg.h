// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vsmoke_tb.h for the primary calling header

#ifndef _VSMOKE_TB_TBLINK_PKG_H_
#define _VSMOKE_TB_TBLINK_PKG_H_  // guard

#include "verilated_heavy.h"
#include "Vsmoke_tb__Dpi.h"

//==========

class Vsmoke_tb__Syms;

//----------

VL_MODULE(Vsmoke_tb_tblink_pkg) {
  public:
    
    // INTERNAL VARIABLES
  private:
    Vsmoke_tb__Syms* __VlSymsp;  // Symbol table
  public:
    
    // CONSTRUCTORS
  private:
    VL_UNCOPYABLE(Vsmoke_tb_tblink_pkg);  ///< Copying not allowed
  public:
    Vsmoke_tb_tblink_pkg(const char* name = "TOP");
    ~Vsmoke_tb_tblink_pkg();
    
    // INTERNAL METHODS
    void __Vconfigure(Vsmoke_tb__Syms* symsp, bool first);
    void __Vdpiimwrap__tblink_dpi_init_TOP__tblink_pkg(const VerilatedScope* __Vscopep, const char* __Vfilenamep, IData/*31:0*/ __Vlineno, IData/*31:0*/ have_blocking_tasks, IData/*31:0*/ (&_tblink_dpi_init__Vfuncrtn));
    void __Vdpiimwrap__tblink_pylist_new_TOP__tblink_pkg(IData/*31:0*/ sz, QData/*63:0*/ (&_tblink_pylist_new__Vfuncrtn));
  private:
    void _ctor_var_reset() VL_ATTR_COLD;
  public:
    static void _initial__TOP__tblink_pkg__1(Vsmoke_tb__Syms* __restrict vlSymsp) VL_ATTR_COLD;
} VL_ATTR_ALIGNED(VL_CACHE_LINE_BYTES);

//----------


#endif  // guard

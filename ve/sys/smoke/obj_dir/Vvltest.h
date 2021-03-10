// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Primary design header
//
// This header should be included by all source files instantiating the design.
// The class here is then constructed to instantiate the design.
// See the Verilator manual for examples.

#ifndef _VVLTEST_H_
#define _VVLTEST_H_  // guard

#include "verilated_heavy.h"

//==========

class Vvltest__Syms;
class Vvltest_cls_pkg;
class Vvltest_cls_pkg__03a__03apyval_c__Vclpkg;
class Vvltest_cls_pkg__03a__03aparam_c__Vclpkg;
class Vvltest_cls_pkg__03a__03alist_c__Vclpkg;
class Vvltest_cls_pkg__03a__03alist_c;


//----------

VL_MODULE(Vvltest) {
  public:
    // CELLS
    // Public to allow access to /*verilator_public*/ items;
    // otherwise the application code can consider these internals.
    Vvltest_cls_pkg* __PVT__cls_pkg;
    Vvltest_cls_pkg__03a__03apyval_c__Vclpkg* cls_pkg__03a__03apyval_c__Vclpkg;
    Vvltest_cls_pkg__03a__03aparam_c__Vclpkg* cls_pkg__03a__03aparam_c__Vclpkg;
    Vvltest_cls_pkg__03a__03alist_c__Vclpkg* cls_pkg__03a__03alist_c__Vclpkg;
    
    // PORTS
    // The application code writes and reads these signals to
    // propagate new values into/out from the Verilated model.
    VL_IN8(clock,0,0);
    
    // LOCAL SIGNALS
    // Internals; generally not touched by application code
    VlClassRef<Vvltest_cls_pkg__03a__03alist_c> top__DOT__unnamedblk1__DOT__l;
    
    // INTERNAL VARIABLES
    // Internals; generally not touched by application code
    Vvltest__Syms* __VlSymsp;  // Symbol table
    
    // CONSTRUCTORS
  private:
    VL_UNCOPYABLE(Vvltest);  ///< Copying not allowed
  public:
    /// Construct the model; called by application code
    /// The special name  may be used to make a wrapper with a
    /// single model invisible with respect to DPI scope names.
    Vvltest(const char* name = "TOP");
    /// Destroy the model; called (often implicitly) by application code
    ~Vvltest();
    
    // API METHODS
    /// Evaluate the model.  Application must call when inputs change.
    void eval() { eval_step(); }
    /// Evaluate when calling multiple units/models per time step.
    void eval_step();
    /// Evaluate at end of a timestep for tracing, when using eval_step().
    /// Application must call after all eval() and before time changes.
    void eval_end_step() {}
    /// Simulation complete, run final blocks.  Application must call on completion.
    void final();
    
    // INTERNAL METHODS
    static void _eval_initial_loop(Vvltest__Syms* __restrict vlSymsp);
    void __Vconfigure(Vvltest__Syms* symsp, bool first);
  private:
    static QData _change_request(Vvltest__Syms* __restrict vlSymsp);
    static QData _change_request_1(Vvltest__Syms* __restrict vlSymsp);
    void _ctor_var_reset() VL_ATTR_COLD;
  public:
    static void _eval(Vvltest__Syms* __restrict vlSymsp);
  private:
#ifdef VL_DEBUG
    void _eval_debug_assertions();
#endif  // VL_DEBUG
  public:
    static void _eval_initial(Vvltest__Syms* __restrict vlSymsp) VL_ATTR_COLD;
    static void _eval_settle(Vvltest__Syms* __restrict vlSymsp) VL_ATTR_COLD;
    static void _initial__TOP__1(Vvltest__Syms* __restrict vlSymsp) VL_ATTR_COLD;
} VL_ATTR_ALIGNED(VL_CACHE_LINE_BYTES);

//----------


#endif  // guard

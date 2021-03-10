// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vsmoke_tb__Syms.h"
#include "Vsmoke_tb.h"
#include "Vsmoke_tb_tblink_pkg.h"



// FUNCTIONS
Vsmoke_tb__Syms::Vsmoke_tb__Syms(Vsmoke_tb* topp, const char* namep)
    // Setup locals
    : __Vm_namep(namep)
    , __Vm_didInit(false)
    // Setup submodule names
    , TOP__tblink_pkg(Verilated::catName(topp->name(), "tblink_pkg"))
{
    // Pointer to top level
    TOPp = topp;
    // Setup each module's pointers to their submodules
    TOPp->__PVT__tblink_pkg = &TOP__tblink_pkg;
    // Setup each module's pointer back to symbol table (for public functions)
    TOPp->__Vconfigure(this, true);
    TOP__tblink_pkg.__Vconfigure(this, true);
    // Setup scopes
    __Vscope_tblink_pkg.configure(this, name(), "tblink_pkg", "tblink_pkg", -12, VerilatedScope::SCOPE_OTHER);
    
    // Setup scope hierarchy
    
    // Setup export functions
    for (int __Vfinal=0; __Vfinal<2; __Vfinal++) {
    }
}

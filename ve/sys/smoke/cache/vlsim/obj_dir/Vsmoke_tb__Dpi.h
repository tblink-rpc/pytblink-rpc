// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Prototypes for DPI import and export functions.
//
// Verilator includes this file in all generated .cpp files that use DPI functions.
// Manually include this file where DPI .c import functions are declared to ensure
// the C functions match the expectations of the DPI imports.

#include "svdpi.h"

#ifdef __cplusplus
extern "C" {
#endif
    
    
    // DPI IMPORTS
    // DPI import at /project/fun/pytblink/pytblink/src/tblink/hvl/tblink_pkg.sv:17:38
    extern int _tblink_dpi_init(int have_blocking_tasks);
    // DPI import at /project/fun/pytblink/pytblink/src/tblink/hvl/tblink_pkg.sv:21:34
    extern void* _tblink_pylist_new(unsigned int sz);
    
#ifdef __cplusplus
}
#endif

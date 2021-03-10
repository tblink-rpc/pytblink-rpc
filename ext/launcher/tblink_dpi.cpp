/*****************************************************************************
 * tblink_dpi.cpp
 *
 * Implements interface routines specific to SystemVerilog
 *
 *  Created on: Dec 13, 2020
 *      Author: mballance
 *****************************************************************************/
#define EXTERN_C extern "C"

extern "C" {
void *svGetScope();
void *svSetScope(void *);
}

// DPI scope handle to the package context
static void *prv_tblink_pkg_s = 0;


EXTERN_C int _tblink_dpi_init(void) {
	// Cache the package scope for later use
	prv_tblink_pkg_s = svGetScope();

	// TODO: launch

	return 0;
}






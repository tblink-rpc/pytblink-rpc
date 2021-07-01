/*****************************************************************************
 * tblink_vpi.cpp
 *
 * Implements interface routines specific to Verilog VPI
 *
 *  Created on: Mar 10, 2021
 *      Author: mballance
 *
 *****************************************************************************/
#define EXTERN_C extern "C"
#include <stdio.h>
#include <string.h>
#include "vpi_user.h"
#include "vpi_api.h"
#include "BackendVpi.h"
#include "PyLauncher.h"

/**
 * Need to provide Py tasks
 * $tblink_py_call("abc", "")
 * $tblink_py_fork("abc", "")
 */

using namespace tblink;

static PyLauncherUP				prv_launcher;
static BackendVpi				*prv_backend;

static PLI_INT32 on_startup(p_cb_data cbd) {
    vpi_api_t *vpi_api = get_vpi_api();

	if (!prv_launcher->start()) {
		// Halt simulation on error
		vpi_api->vpi_control(vpiFinish, 1);
	}

	return 0;
}

static void register_tblink_tf(void) {
	s_cb_data cbd;
    vpi_api_t *vpi_api = get_vpi_api();

    if (!vpi_api) {
    	fprintf(stdout, "Error: failed to load VPI API (%s)\n",
    			get_vpi_api_error());
    	return;
    }

	memset(&cbd, 0, sizeof(cbd));
	cbd.reason = cbStartOfSimulation;
	cbd.cb_rtn = &on_startup;
	vpi_api->vpi_register_cb(&cbd);

    prv_backend = new BackendVpi(vpi_api);
    prv_launcher = PyLauncherUP(new PyLauncher(prv_backend));

    // TODO: register callbacks to do actual launch

}

void (*vlog_startup_routines[])() = {
	register_tblink_tf,
    0
};


// For non-VPI compliant applications that cannot find vlog_startup_routines symbol
void vlog_startup_routines_bootstrap() {
    for (int i = 0; vlog_startup_routines[i]; i++) {
    	void (*routine)() = vlog_startup_routines[i];
        routine();
    }
}


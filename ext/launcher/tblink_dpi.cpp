
/*****************************************************************************
 * tblink_dpi.cpp
 *
 * Implements interface routines specific to SystemVerilog
 *
 *  Created on: Dec 13, 2020
 *      Author: mballance
 *****************************************************************************/
#define EXTERN_C extern "C"
#include <stdio.h>
#include "vpi_user.h"
#include <string>
#include <vector>
#include "BackendDpi.h"
#include "PyLauncher.h"
#include <Python.h>
#include <memory>
#include "vpi_api.h"


// Externs for DPI-Exported methods

using namespace tblink;

static PyLauncherUP		prv_launcher;
static BackendDpi		*prv_backend;

EXTERN_C int _tblink_dpi_init(int32_t have_blocking_tasks) {
	vpi_api_t *vpi_api = get_vpi_api();

	if (!vpi_api) {
		fprintf(stdout, "Error: failed to load vpi API (%s)\n",
				get_vpi_api_error());
		return 0;
	}

	prv_backend = new BackendDpi(vpi_api, have_blocking_tasks);
	prv_launcher = PyLauncherUP(new PyLauncher(prv_backend));

	if (prv_launcher->start()) {
		return 1;
	} else {
		return 0;
	}
}

EXTERN_C void _tblink_timed_callback(int id) {
	prv_backend->timed_callback(id);
}

EXTERN_C void *_tblink_pylist_new(unsigned int sz) {
	return PyList_New(sz);
}


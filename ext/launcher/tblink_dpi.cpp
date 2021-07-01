
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
#include <dlfcn.h>
#include <memory>
#include "vpi_api.h"


// Externs for DPI-Exported methods
extern "C" {
void *svGetScope() __attribute__((weak));
void *svSetScope(void *) __attribute__((weak));
int _tblink_register_timed_callback(uint64_t delta) __attribute__((weak));

void *svGetScope() {
	return 0;
}

void *svSetScope(void *) {
	return 0;
}

int _tblink_register_timed_callback(uint64_t delta) {
	return -1;
}

}


using namespace tblink;

static PyLauncherUP		prv_launcher;
static BackendDpi		*prv_backend;

EXTERN_C int _tblink_dpi_init(int32_t have_blocking_tasks) {
	vpi_api_t *vpi_api = get_vpi_api();

	fprintf(stdout, "_tblink_dpi_init\n");
	fflush(stdout);

	{
		void *lib = dlopen(0, RTLD_LAZY);
		void *sym = dlsym(lib, "_tblink_register_timed_callback");
		fprintf(stdout, "lib=%p sym=%p\n");
		fflush(stdout);
	}

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

EXTERN_C int _tblink_dpi_register_scope(const char *s) {
	fprintf(stdout, "register_scope: %s %p\n", s, prv_backend);
	if (prv_backend) {
		prv_backend->register_scope(s, svGetScope());
		return 1;
	} else {
		return 0;
	}
}

EXTERN_C void _tblink_timed_callback(int id) {
	fprintf(stdout, "tblink_timed_callback\n");
	fflush(stdout);
	prv_backend->timed_callback(id);
}

EXTERN_C void *_tblink_pylist_new(unsigned int sz) {
	return PyList_New(sz);
}


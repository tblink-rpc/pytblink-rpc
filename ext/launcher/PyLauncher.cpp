/*
 * PyLauncher.cpp
 *
 *  Created on: Dec 13, 2020
 *      Author: mballance
 */

#include "PyLauncher.h"

namespace tblink {

PyLauncher::PyLauncher(IBackend *backend) : m_backend(backend) {
	// TODO Auto-generated constructor stub

}

PyLauncher::~PyLauncher() {
	// TODO Auto-generated destructor stub
}

bool PyLauncher::start() {
	bool ret = true;

	Py_Initialize();

	if (!(m_interp = Py_NewInterpreter())) {
		return false;
	}

	fprintf(stdout, "interp=%p\n", m_interp);

	// Load up the core tblink module
	if (!(m_tblink = PyImport_ImportModule("tblink"))) {
		fprintf(stdout, "Failed to load tblink\n");
		return false;
	}

	PyObject *tblink_core;

	if (!(tblink_core = PyImport_ImportModule("tblink_core"))) {
		fprintf(stdout, "Failed to load tblink_core\n");
		return false;
	}

	fprintf(stdout, "tblink=%p\n", m_tblink);

	PyObject *backend = PyObject_CallMethod(tblink_core, "BackendNative",
			"(K)", reinterpret_cast<uint64_t>(m_backend));

	// Perform zero-time initialization
	if (!PyObject_CallMethod(m_tblink, "init", "(O)", backend)) {
		PyErr_PrintEx(0);
		return false;
	}

	// Launch entry-point
	fprintf(stdout, "--> Call: entry\n");
	if (!PyObject_CallMethod(m_tblink, "start", "")) {
		PyErr_PrintEx(0);
		return false;
	}
	fprintf(stdout, "<-- Call: entry\n");

//	fprintf(stdout, "--> Call: reschedule\n");
//	if (!PyObject_CallMethod(m_tblink, "reschedule", "")) {
//		PyErr_PrintEx(0);
//		return false;
//	}
//	fprintf(stdout, "<-- Call: reschedule\n");

	return true;
}

} /* namespace tblink */

/*
 * PyLauncher.h
 *
 *  Created on: Dec 13, 2020
 *      Author: mballance
 */

#pragma once
#include <memory>
#include <string>
#include <vector>
#include "IBackend.h"
#include <Python.h>

namespace tblink {

class PyLauncher {
public:
	PyLauncher(IBackend *backend);

	virtual ~PyLauncher();

	bool start();

private:
	IBackend								*m_backend;
	bool									m_supports_blocking_tasks;
	std::vector<std::string>				m_args;
	PyThreadState							*m_interp;
	PyObject								*m_tblink;

};

typedef std::unique_ptr<PyLauncher> PyLauncherUP;

} /* namespace tblink */


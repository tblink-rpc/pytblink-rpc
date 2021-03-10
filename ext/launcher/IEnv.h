/*
 * IEnv.h
 *
 *  Created on: Dec 13, 2020
 *      Author: mballance
 */

#pragma once
#include <stdint.h>

class PyLauncher;

class IEnv {
public:

	virtual ~IEnv() { }

	virtual void init(PyLauncher *l) = 0;

//	virtual void

};

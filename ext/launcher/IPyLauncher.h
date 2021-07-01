/*
 * IPyLauncher.h
 *
 *  Created on: Apr 1, 2021
 *      Author: mballance
 */

#pragma once
#include "IEndpoint.h"

namespace tblink {

class IPyLauncher : public virtual IEndpoint {
public:

	virtual ~IPyLauncher() { }

	virtual bool start() = 0;

};

}



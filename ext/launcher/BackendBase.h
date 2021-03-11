/*
 * BackendBase.h
 *
 *  Created on: Mar 8, 2021
 *      Author: mballance
 */

#pragma once
#include "../launcher/IBackend.h"

namespace tblink {

class BackendBase : public virtual IBackend {
public:
	BackendBase();

	virtual ~BackendBase();

};

} /* namespace tblink */


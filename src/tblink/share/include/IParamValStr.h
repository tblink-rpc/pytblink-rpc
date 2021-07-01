/*
 * IParamValStr.h
 *
 *  Created on: Apr 3, 2021
 *      Author: mballance
 */

#pragma once
#include "IParamVal.h"

namespace tblink {

class IParamValStr;
typedef std::shared_ptr<IParamValStr> IParamValStrSP;
class IParamValStr : public virtual IParamVal {
public:
	virtual ~IParamValStr() { }

	virtual std::string val() = 0;

};

}

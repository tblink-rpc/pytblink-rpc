/*
 * IParamVal.h
 *
 *  Created on: Apr 3, 2021
 *      Author: mballance
 */

#pragma once
#include <memory>

namespace tblink {

class IParamVal;
typedef std::shared_ptr<IParamVal> IParamValSP;
class IParamVal {
public:

	virtual ~IParamVal() { }

};


}


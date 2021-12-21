/*
 * IApiMethod.h
 *
 *  Created on: Apr 4, 2021
 *      Author: mballance
 */

#pragma once
#include <memory>

namespace tblink {

class IApiMethod;
typedef std::shared_ptr<IApiMethod> IApiMethodSP;
class IApiMethod {
public:

	virtual ~IApiMethod() { }

	virtual const std::string &name() const = 0;

//	virtual const std::string &signature() const = 0;

};

}


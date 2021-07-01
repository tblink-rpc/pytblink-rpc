/*
 * ApiMethod.h
 *
 *  Created on: Apr 6, 2021
 *      Author: mballance
 */

#pragma once
#include <string>
#include "IApiMethod.h"

namespace tblink {

class ApiMethod;
typedef std::shared_ptr<ApiMethod> ApiMethodSP;
class ApiMethod : public IApiMethod {
public:
	ApiMethod(const std::string &name);

	virtual ~ApiMethod();

	virtual const std::string &name() const {
		return m_name;
	}

private:
	std::string					m_name;
};

} /* namespace tblink */


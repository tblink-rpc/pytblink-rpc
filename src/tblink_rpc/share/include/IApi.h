/*
 * IApi.h
 *
 *  Created on: Apr 3, 2021
 *      Author: mballance
 */

#pragma once
#include "IApiMethod.h"

namespace tblink {

class IEndpoint;

class IApi;
typedef std::shared_ptr<IApi> IApiSP;
class IApi {
public:

	virtual ~IApi() { }

	virtual const std::string &id() const = 0;

	virtual const bool is_import() const = 0;

	virtual IApiMethodSP add_method(const std::string &name) = 0;

	virtual IApiMethodSP get_method(const std::string &name) = 0;

};

}


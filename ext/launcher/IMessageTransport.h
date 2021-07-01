/*
 * IMessageTransport.h
 *
 *  Created on: Sep 21, 2020
 *      Author: ballance
 */

#pragma once
#include <string>
#include "nlohmann/json_fwd.hpp"
#include "JsonParamVal.h"

namespace tblink {

class IMessageTransport {
public:
	virtual ~IMessageTransport() { }

	virtual int32_t send(
			const std::string	&method,
			JsonParamValSP		params) = 0;

	virtual void recv(const nlohmann::json &msg) = 0;

};

} /* namespace tblink */



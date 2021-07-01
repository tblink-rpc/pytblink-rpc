/*
 * IRegisterMethod.h
 *
 *  Created on: Oct 1, 2020
 *      Author: ballance
 */

#pragma once
#include <string>
#include <functional>
#include "nlohmann/json_fwd.hpp"

namespace tblink {

class IRegisterMethod {
public:
	virtual ~IRegisterMethod() { }

	virtual void register_method(
			const std::string							&method,
			std::function<void(const nlohmann::json &)> impl) = 0;

};

}

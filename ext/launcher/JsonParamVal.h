/*
 * Val.h
 *
 *  Created on: Sep 30, 2020
 *      Author: ballance
 */

#pragma once
#include <memory>
#include "nlohmann/json_fwd.hpp"
#include "IParamVal.h"

namespace tblink {

class JsonParamVal;
typedef std::shared_ptr<JsonParamVal> JsonParamValSP;

class JsonParamVal : public virtual IParamVal {
public:
	JsonParamVal();

	virtual ~JsonParamVal();

	virtual nlohmann::json dump();

	static JsonParamValSP load(const nlohmann::json &msg);

};


} /* namespace tblink */


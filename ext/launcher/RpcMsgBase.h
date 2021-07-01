/*
 * RpcMsgBase.h
 *
 *  Created on: Apr 7, 2021
 *      Author: mballance
 */

#pragma once
#include "JsonParamVal.h"
#include "JsonParamValInt.h"
#include "JsonParamValStr.h"
#include "nlohmann/json_fwd.hpp"

namespace tblink {

class RpcMsgBase : public JsonParamVal {
public:
	RpcMsgBase(
			int32_t				id,
			const std::string	&method);

	virtual ~RpcMsgBase();

	virtual nlohmann::json dump() override;

protected:
	JsonParamValIntSP			m_id;
	JsonParamValStrSP			m_method;

};

} /* namespace tblink */


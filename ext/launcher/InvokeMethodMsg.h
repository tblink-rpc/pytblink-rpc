/*
 * InvokeMethodMsg.h
 *
 *  Created on: Apr 7, 2021
 *      Author: mballance
 */

#pragma once
#include "RpcMsgBase.h"
#include "JsonParamValInt.h"
#include "JsonParamValStr.h"
#include "JsonParamValVectorBase.h"
#include "nlohmann/json_fwd.hpp"

namespace tblink {

class InvokeMethodMsg;
typedef std::shared_ptr<InvokeMethodMsg> InvokeMethodMsgSP;
class InvokeMethodMsg : public RpcMsgBase {
public:
	InvokeMethodMsg(
			int32_t							bundle_id,
			int32_t							api_id,
			int32_t							method_id,
			JsonParamValVectorBaseSP		params);

	virtual ~InvokeMethodMsg();

	virtual nlohmann::json dump() override;

private:
	JsonParamValIntSP						m_bundle_id;
	JsonParamValIntSP						m_api_id;
	JsonParamValIntSP						m_method_id;
	JsonParamValVectorBaseSP				m_params;

};

} /* namespace tblink */


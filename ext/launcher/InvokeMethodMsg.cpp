/*
 * InvokeMethodMsg.cpp
 *
 *  Created on: Apr 7, 2021
 *      Author: mballance
 */

#include "InvokeMethodMsg.h"
#include "nlohmann/json.hpp"

namespace tblink {

InvokeMethodMsg::InvokeMethodMsg(
		int32_t						bundle_id,
		int32_t						api_id,
		int32_t						method_id,
		JsonParamValVectorBaseSP	params) :
			RpcMsgBase(0, "invoke-method"),
			m_bundle_id(JsonParamValInt::mk(bundle_id)),
			m_api_id(JsonParamValInt::mk(api_id)),
			m_method_id(JsonParamValInt::mk(method_id)),
			m_params(params) {
	// TODO Auto-generated constructor stub

}

InvokeMethodMsg::~InvokeMethodMsg() {
	// TODO Auto-generated destructor stub
}

nlohmann::json InvokeMethodMsg::dump() {
	nlohmann::json msg;

	msg["bundle-id"] = m_bundle_id->dump();
	msg["api-id"] = m_api_id->dump();
	msg["method-id"] = m_method_id->dump();
	msg["params"] = m_params->dump();

	return msg;
}

} /* namespace tblink */

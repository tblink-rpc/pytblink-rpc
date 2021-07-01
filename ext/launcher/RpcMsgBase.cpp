/*
 * RpcMsgBase.cpp
 *
 *  Created on: Apr 7, 2021
 *      Author: mballance
 */

#include "RpcMsgBase.h"
#include "nlohmann/json.hpp"

namespace tblink {

RpcMsgBase::RpcMsgBase(
		int32_t				id,
		const std::string	&method) :
			m_id(JsonParamValInt::mk(id)),
			m_method(JsonParamValStr::mk(method)) {

}

RpcMsgBase::~RpcMsgBase() {
	// TODO Auto-generated destructor stub
}

nlohmann::json RpcMsgBase::dump() {
	nlohmann::json msg;

	msg["id"] = m_id->dump();
	msg["method"] = m_method->dump();

	return msg;
}

} /* namespace tblink */

/*
 * InitializeReq.cpp
 *
 *  Created on: Mar 31, 2021
 *      Author: mballance
 */

#include "InitializeReq.h"
#include "nlohmann/json.hpp"

namespace tblink {

InitializeReq::InitializeReq(const nlohmann::json &msg) {
	// TODO Auto-generated constructor stub

}

InitializeReq::~InitializeReq() {
	// TODO Auto-generated destructor stub
}

nlohmann::json InitializeReq::dump() {
	nlohmann::json msg;

	if (m_module) {
		msg["module"] = m_module->dump();
	}

	if (m_entry) {
		msg["entry"] = m_entry->dump();
	}

	return msg;
}

InitializeReqSP InitializeReq::load(const nlohmann::json &msg) {
	return InitializeReqSP(new InitializeReq(msg));
}

} /* namespace tblink */

/*
 * InitializeRsp.cpp
 *
 *  Created on: Mar 31, 2021
 *      Author: mballance
 */

#include "InitializeRsp.h"
#include "nlohmann/json.hpp"

namespace tblink {

InitializeRsp::InitializeRsp() :
	m_apis(JsonParamValVector<ApiDef>::mk()) {
	// TODO Auto-generated constructor stub

}

InitializeRsp::~InitializeRsp() {
	// TODO Auto-generated destructor stub
}

nlohmann::json InitializeRsp::dump() {
	nlohmann::json msg;

	msg["apis"] = m_apis->dump();

	return msg;
}

InitializeRspSP InitializeRsp::mk() {
	return InitializeRspSP(new InitializeRsp());
}

} /* namespace tblink */

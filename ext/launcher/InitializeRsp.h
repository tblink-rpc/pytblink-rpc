/*
 * InitializeRsp.h
 *
 *  Created on: Mar 31, 2021
 *      Author: mballance
 */

#pragma once
#include "ApiDef.h"
#include "JsonParamVal.h"
#include "JsonParamValVector.h"

namespace tblink {

class InitializeRsp;
typedef std::shared_ptr<InitializeRsp> InitializeRspSP;
class InitializeRsp : public JsonParamVal {
public:
	InitializeRsp();

	virtual ~InitializeRsp();

	virtual nlohmann::json dump();

	static InitializeRspSP mk();

private:
	JsonParamValVector<ApiDef>::SP			m_apis;

};

} /* namespace tblink */


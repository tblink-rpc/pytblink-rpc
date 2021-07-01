/*
 * InitializeReq.h
 *
 *  Created on: Mar 31, 2021
 *      Author: mballance
 */

#pragma once
#include "JsonParamVal.h"
#include "JsonParamValStr.h"

namespace tblink {

class InitializeReq;
typedef std::shared_ptr<InitializeReq> InitializeReqSP;
class InitializeReq : public JsonParamVal{
public:
	InitializeReq(const nlohmann::json &msg);

	virtual ~InitializeReq();

	nlohmann::json dump();

	static InitializeReqSP load(const nlohmann::json &msg);

private:
	JsonParamValStrSP				m_module;
	JsonParamValStrSP				m_entry;


};

} /* namespace tblink */


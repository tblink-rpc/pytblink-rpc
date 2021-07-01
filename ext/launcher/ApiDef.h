/*
 * ApiDef.h
 *
 *  Created on: Mar 31, 2021
 *      Author: mballance
 */

#pragma once
#include "JsonParamVal.h"

namespace tblink {

class ApiDef;
typedef std::shared_ptr<ApiDef> ApiDefSP;
class ApiDef : public JsonParamVal {
public:
	ApiDef();

	virtual ~ApiDef();
};

} /* namespace tblink */


/*
 * ValVector.cpp
 *
 *  Created on: Oct 1, 2020
 *      Author: ballance
 */

#include "JsonParamValVectorBase.h"

#include "nlohmann/json.hpp"

namespace tblink {

JsonParamValVectorBase::JsonParamValVectorBase() {

}

JsonParamValVectorBase::JsonParamValVectorBase(
		std::function<JsonParamValSP(const nlohmann::json &)> 	ctor,
		const nlohmann::json							&msg) {
	/*
	for (uint32_t i=0; ; ) {
		ValSP v = ctor(msg);
	}
	 */

}

JsonParamValVectorBase::~JsonParamValVectorBase() {
	// TODO Auto-generated destructor stub
}

void JsonParamValVectorBase::push_back(IParamValSP v) {
	m_children.push_back(std::dynamic_pointer_cast<JsonParamVal>(v));
}

nlohmann::json JsonParamValVectorBase::dump() {
	nlohmann::json msg;

	return msg;
}

JsonParamValVectorBaseSP JsonParamValVectorBase::mk(
			std::function<JsonParamValSP(const nlohmann::json &)> 	ctor,
			const nlohmann::json 							&msg) {
	return JsonParamValVectorBaseSP(new JsonParamValVectorBase(ctor, msg));
}

} /* namespace tblink */

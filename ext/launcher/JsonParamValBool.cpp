/*
 * ValBool.cpp
 *
 *  Created on: Oct 3, 2020
 *      Author: ballance
 */

#include "JsonParamValBool.h"

#include "nlohmann/json.hpp"

namespace tblink {

JsonParamValBool::JsonParamValBool(bool v) : m_val(v) {

}

JsonParamValBool::JsonParamValBool(const nlohmann::json &msg) {
	m_val = msg.get<bool>();
}

JsonParamValBool::~JsonParamValBool() {
	// TODO Auto-generated destructor stub
}

nlohmann::json JsonParamValBool::dump() {
	return nlohmann::json(m_val);
}

ValBoolSP JsonParamValBool::mk(bool v) {
	return ValBoolSP(new JsonParamValBool(v));
}

ValBoolSP JsonParamValBool::mk(const nlohmann::json &msg) {
	return ValBoolSP(new JsonParamValBool(msg));
}

const ValBoolSP	JsonParamValBool::true_v(new JsonParamValBool(true));
const ValBoolSP	JsonParamValBool::false_v(new JsonParamValBool(false));

} /* namespace tblink */

/*
 * ValStr.cpp
 *
 *  Created on: Sep 30, 2020
 *      Author: ballance
 */

#include "JsonParamValStr.h"

#include "nlohmann/json.hpp"

namespace tblink {

JsonParamValStr::JsonParamValStr(const nlohmann::json &msg) {
	m_val = msg.get<std::string>();
}

JsonParamValStr::JsonParamValStr(const std::string &v) : m_val(v) {

}

JsonParamValStr::~JsonParamValStr() {
	// TODO Auto-generated destructor stub
}

nlohmann::json JsonParamValStr::dump() {
	return nlohmann::json(m_val);
}

JsonParamValStrSP JsonParamValStr::mk(const nlohmann::json &msg) {
	return JsonParamValStrSP(new JsonParamValStr(msg));
}

JsonParamValStrSP JsonParamValStr::mk(const std::string &v) {
	return JsonParamValStrSP(new JsonParamValStr(v));
}

} /* namespace tblink */

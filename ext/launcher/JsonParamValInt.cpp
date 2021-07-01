/*
 * ValInt.cpp
 *
 *  Created on: Oct 1, 2020
 *      Author: ballance
 */

#include "JsonParamValInt.h"

#include "nlohmann/json.hpp"

namespace tblink {

JsonParamValInt::JsonParamValInt(int64_t v) : m_val(v){

}

JsonParamValInt::JsonParamValInt(const nlohmann::json &msg) {
	if (msg.is_number()) {
		m_val = msg;
	} else if (msg.is_string()) {
		m_val =std::stoi(msg.get<std::string>());
	} else {
		// ERROR
		m_val = -1;
	}
}

JsonParamValInt::~JsonParamValInt() {
	// TODO Auto-generated destructor stub
}

nlohmann::json JsonParamValInt::dump() {
	return nlohmann::json(m_val);
}

JsonParamValIntSP JsonParamValInt::mk(const nlohmann::json &msg) {
	if (msg.is_number()) {
		return JsonParamValIntSP(new JsonParamValInt(msg));
	} else if (msg.is_string()) {
		return JsonParamValIntSP(new JsonParamValInt(std::stoi(msg.get<std::string>())));
	} else {
		// ERROR
		return JsonParamValIntSP(new JsonParamValInt(-1));
	}
}

JsonParamValIntSP JsonParamValInt::mk(int32_t v) {
	return JsonParamValIntSP(new JsonParamValInt(v));
}

} /* namespace tblink */

/*
 * Message.cpp
 *
 *  Created on: Sep 29, 2020
 *      Author: ballance
 */

#include "Message.h"
#include "nlohmann/json.hpp"

namespace tblink {

Message::Message(const nlohmann::json &msg) {
	;
}

Message::Message() : m_jsonrpc("2.0") {
	// TODO Auto-generated constructor stub

}

Message::~Message() {
	// TODO Auto-generated destructor stub
}

void Message::load(const nlohmann::json &msg) {
	m_jsonrpc = msg["jsonrpc"];
}

void Message::dump(nlohmann::json &msg) {
	msg["jsonrpc"] = m_jsonrpc;
}

int32_t Message::get_int(const nlohmann::json &msg, const std::string &key) {
	int32_t ret = 0;
	if (msg["id"].type() == nlohmann::json::value_t::number_integer) {
		ret = msg["id"];
	} else {
		ret = std::stoi(msg["id"].get<std::string>());
	}
	return ret;
}

} /* namespace tblink */

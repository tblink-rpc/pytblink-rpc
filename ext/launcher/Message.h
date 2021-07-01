/*
 * Message.h
 *
 *  Created on: Sep 29, 2020
 *      Author: ballance
 */

#pragma once
#include <stdint.h>
#include "nlohmann/json_fwd.hpp"

namespace tblink {

class Message {
public:
	Message(const nlohmann::json &msg);

	Message();

	virtual ~Message();

	virtual void load(const nlohmann::json &msg);

	virtual void dump(nlohmann::json &msg);

protected:
	int32_t get_int(const nlohmann::json &msg, const std::string &key);

protected:
	std::string				m_jsonrpc;

};

} /* namespace tblink */


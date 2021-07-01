/*
 * MessageDispatcher.h
 *
 *  Created on: Oct 1, 2020
 *      Author: ballance
 */

#pragma once
#include <functional>
#include <map>
#include "IMessageTransport.h"
#include "IRegisterMethod.h"
#include "JsonParamVal.h"

namespace tblink {

class MessageDispatcher;
typedef std::unique_ptr<MessageDispatcher> MessageDispatcherUP;
class MessageDispatcher :
		public virtual IMessageTransport,
		public virtual IRegisterMethod {
public:
	MessageDispatcher();

	virtual ~MessageDispatcher();

	void register_method(
			const std::string							&method,
			std::function<void(const nlohmann::json &)>	impl) override;

	virtual int32_t send(
			const std::string		&method,
			JsonParamValSP			params) override { }

	/**
	 * Inbound message
	 */
	virtual void recv(const nlohmann::json &msg) override;

private:
	std::map<std::string,std::function<void(const nlohmann::json &)>> m_method_m;
};

} /* namespace tblink */


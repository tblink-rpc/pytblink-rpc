/*
 * SocketMessageTransport.h
 *
 *  Created on: Sep 21, 2020
 *      Author: ballance
 */

#pragma once
#include <string>
#include "IMessageTransport.h"
#include "nlohmann/json_fwd.hpp"

namespace tblink {

class SocketMessageTransport : public IMessageTransport {
public:
	SocketMessageTransport(
			int32_t			socket);

	virtual ~SocketMessageTransport();

	void init(IMessageTransport *in);

	int32_t process(int32_t timeout_ms=-1);

	virtual void recv(const nlohmann::json &msg) override { }

	virtual int32_t send(
			const std::string	&method,
			JsonParamValSP		params) override;

private:
	void msgbuf_append(char c) {
		if (m_msgbuf_idx+1 < m_msgbuf_max) {
			m_msgbuf[m_msgbuf_idx++] = c;
		} else {
			msgbuf_resize_append(c);
		}
	}

	void msgbuf_resize_append(char c);

private:
	char						*m_msgbuf;
	int32_t						m_id;
	uint32_t					m_msgbuf_idx;
	uint32_t					m_msgbuf_max;
	uint32_t					m_msg_state;
	uint32_t					m_msg_length;
	int32_t						m_socket;
	IMessageTransport			*m_in;

	static const std::string	HEADER_PREFIX;

};

} /* namespace tblink */


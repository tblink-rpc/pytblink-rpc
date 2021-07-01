/*
 * PyLauncher.h
 *
 *  Created on: Dec 13, 2020
 *      Author: mballance
 */

#pragma once
#include <memory>
#include <string>
#include <vector>
#include "IBackend.h"
#include "IPyLauncher.h"
#include "MessageDispatcher.h"
#include "SocketMessageTransport.h"

namespace tblink {

class SocketMessageTransport;
typedef std::unique_ptr<SocketMessageTransport> SocketMessageTransportUP;

class PyLauncher : public IPyLauncher {
public:
	PyLauncher(IBackend *backend);

	virtual ~PyLauncher();

	virtual bool start() override;

	/**
	 * Phasing-control methods
	 */

	// Note, likely need blocking and non-blocking endpoints

	/**
	 * Notify that build in this environment is complete
	 */
	virtual bool build_complete() override;

	/**
	 * Notify that connect in this environment is complete
	 */
	virtual bool connect_complete() override;

	/**
	 * Registers an API expected to be implemented
	 * by the connected environment
	 */
	virtual void add_import(IApiSP api) override;

	/**
	 * Registers an API that this environment implements
	 */
	virtual void add_export(
			IApiSP 				api,
			IApiExportSP		impl) override;

	virtual void set_export_impl(
			IApiSP 				api,
			IApiExportSP		impl) override;

	virtual IParamValVectorSP mkParamValVector() override;

	virtual IParamValIntSP mkParamValInt(
			uint64_t			val,
			bool				is_signed,
			int32_t				width=-1) override;

	virtual IParamValStrSP mkParamValStr(const std::string &v);

	/**
	 * Invokes a method, calling the completion function when
	 * the call is complete
	 */
	virtual void invoke_method_async(
			IApiMethodSP								method,
			IParamValVectorSP							params,
			const std::function<void (IParamValSP)>		&completion) override;

	/**
	 * Invokes a method and returns the return value
	 */
	virtual IParamValSP invoke_method(
			IApiMethodSP								method,
			IParamValVectorSP							params) override;

private:

	std::string find_python();

	void register_methods();

	void initialize_req(const nlohmann::json &msg);

	static void init_cb(void *ud);

	void init_cb();

private:
	IBackend								*m_backend;
	bool									m_supports_blocking_tasks;
	std::vector<std::string>				m_args;
	int32_t									m_srv_socket;
	int32_t									m_conn_socket;
	MessageDispatcherUP						m_dispatcher;
	SocketMessageTransportUP				m_transport;
	pid_t									m_pid;

	bool									m_received_init;

};

typedef std::unique_ptr<PyLauncher> PyLauncherUP;

} /* namespace tblink */


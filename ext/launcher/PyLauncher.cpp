/*
 * PyLauncher.cpp
 *
 *  Created on: Dec 13, 2020
 *      Author: mballance
 */

#include "PyLauncher.h"
#ifndef _WIN32
#include <pthread.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <netdb.h>
#include <netinet/in.h>
#include <sys/stat.h>
#include <fcntl.h>
static const char PS = ':';
#else
#include <winsock2.h>
static const char PS = ';';
#endif
#include <spawn.h>
#include <string.h>

#include "InitializeRsp.h"
#include "nlohmann/json.hpp"

#include "JsonParamValInt.h"
#include "JsonParamValStr.h"
#include "JsonParamValVectorBase.h"

#include "InvokeMethodMsg.h"

extern char **environ;

namespace tblink {

PyLauncher::PyLauncher(IBackend *backend) :
		m_backend(backend), m_received_init(false) {
	// TODO Auto-generated constructor stub

}

PyLauncher::~PyLauncher() {
	// TODO Auto-generated destructor stub
}

bool PyLauncher::start() {
	bool ret = true;
	std::string python;

	// First, locate a Python interpreter
	const char *tblink_python = getenv("TBLINK_PYTHON");

	if (tblink_python && tblink_python[0]) {
		python = tblink_python;
	} else {
		python = find_python();
	}

	if (python == "") {
		fprintf(stdout, "Error: failed to find Python\n");
		return false;
	}

	// Create the socket server
	struct sockaddr_in serv_addr;

	m_srv_socket = socket(AF_INET, SOCK_STREAM, 0);

    memset(&serv_addr, 0, sizeof(serv_addr));

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    serv_addr.sin_port = 0;

    if ((bind(m_srv_socket, (struct sockaddr *)&serv_addr, sizeof(serv_addr))) < 0) {
    	perror("Error binding");
    }

    socklen_t size = sizeof(serv_addr);
    getsockname(m_srv_socket, (struct sockaddr *) &serv_addr, &size);

    fprintf(stdout, "port: %d\n", serv_addr.sin_port);
    fflush(stdout);
//    cd.port = serv_addr.sin_port;
//    ASSERT_EQ(pthread_create(&thread, 0, &client_f, &cd), 0);

    listen(m_srv_socket, 1);

	// Spawn the interpreter
    {
    	std::vector<std::string> args;
    	char tmp[16], hostname[16], m[4], module[16];
    	char *exec_t = (char *)alloca(python.size()+1);

    	strcpy(hostname, "localhost");
    	strcpy(m, "-m");
    	strcpy(module, "tblink.runtime");
    	strcpy(exec_t, python.c_str());

    	sprintf(tmp, "%d", ntohs(serv_addr.sin_port));
    	char **argv = (char **)alloca(sizeof(char *)*6);
    	argv[0] = exec_t;
    	argv[1] = m;
    	argv[2] = module;
    	argv[3] = hostname;
    	argv[4] = tmp;
    	argv[5] = 0;

    	int status = posix_spawnp(&m_pid, argv[0], 0, 0, (char *const *)argv, environ);

    	if (status != 0) {
    		fprintf(stdout, "Error: Failed to launch python \"%s\"\n", python.c_str());
    		return false;
    	}
    }

	// Wait for a connection, or for
	// the interpreter process to exit
    {
    	// Wait for a bit to see if we get a connect request
    	fd_set rfds;
    	struct timeval tv;
    	int retval;


    	/*
    	 * Wait for a connect request for 10ms
    	 * at a time. * Wait up to five seconds total
    	 */
    	for (uint32_t i=0; i<500; i++) {
    		tv.tv_sec = 0;
    		tv.tv_usec = 10000;

    		FD_ZERO(&rfds);
    		FD_SET(m_srv_socket, &rfds);

    		retval = select(m_srv_socket+1, &rfds, 0, 0, &tv);

    		if (retval > 0) {
    			break;
    		} else {
    			// Check that the process is still alive
    			int status;
    			retval = waitpid(m_pid, &status, WNOHANG);

    			// If the process either doesn't exist
    			// or has terminated, then bail out early
    			if (retval != 0) {
    				retval = -1;
    				break;
    			}
    		}
    	}

    	if (retval > 0) {
    		unsigned int clilen = sizeof(serv_addr);
    		m_conn_socket = accept(m_srv_socket, (struct sockaddr *)&serv_addr, &clilen);
    	} else {
    		m_conn_socket = -1;
    	}
    }

    if (m_conn_socket == -1) {
    	fprintf(stdout, "Error: accept failed\n");
    	return false;
    }

    fprintf(stdout, "Note: socket %d\n", m_conn_socket);

#ifdef _WIN32
   unsigned long mode = 0;
   ioctlsocket(m_conn_socket, FIONBIO, &mode);
#else
   int flags = fcntl(m_conn_socket, F_GETFL, 0);
   fcntl(m_conn_socket, F_SETFL, (flags | O_NONBLOCK));
#endif

	m_transport = SocketMessageTransportUP(new SocketMessageTransport(m_conn_socket));
	m_dispatcher = MessageDispatcherUP(new MessageDispatcher());

	register_methods();

	m_transport->init(m_dispatcher.get());

    fprintf(stdout, "connected\n");

    // Process startup messages

    // wait for an InitializeReq message
    int init_status = -1;
    do {
    	while ((init_status=m_transport->process(1000)) > 0) {
    		fprintf(stdout, "init_status=%d\n", init_status);
    		;
    	}

    	fprintf(stdout, "init_status=%d\n", init_status);

//    	if (ret == -1) {
//    		m_received_init = false;
//    	}
    } while (!m_received_init && init_status > 0);

    if (init_status < 0) {
    	int status;
    	fprintf(stdout, "Failed to receive init message\n");

    	// Make a good-faith effort to reap the zombie process
    	waitpid(m_pid, &status, WNOHANG);

    	return false;
    }

    //

    // TODO: Register a zero-time callback to come back to
    if (m_backend) {
    	m_backend->add_simtime_cb(0, &PyLauncher::init_cb, this);
    } else {
    	init_cb();
    }
//    m_backend->

	return true;
}

/**
 * Phasing-control methods
 */

// Note, likely need blocking and non-blocking endpoints

/**
 * Notify that build in this environment is complete
 */
bool PyLauncher::build_complete() { }

/**
 * Notify that connect in this environment is complete
 */
bool PyLauncher::connect_complete() { }

/**
 * Registers an API expected to be implemented
 * by the connected environment
 */
void PyLauncher::add_import(IApiSP api) { }

/**
 * Registers an API that this environment implements
 */
void PyLauncher::add_export(
		IApiSP 				api,
		IApiExportSP		impl) { }

void PyLauncher::set_export_impl(
		IApiSP 				api,
		IApiExportSP		impl) { }

IParamValVectorSP PyLauncher::mkParamValVector() {
	return std::make_shared<JsonParamValVectorBase>();
}

IParamValIntSP PyLauncher::mkParamValInt(
		uint64_t			val,
		bool				is_signed,
		int32_t				width) {
	// TODO:
	return std::make_shared<JsonParamValInt>(val);
}

IParamValStrSP PyLauncher::mkParamValStr(const std::string &v) {
	return std::make_shared<JsonParamValStr>(v);
}

/**
 * Invokes a method, calling the completion function when
 * the call is complete
 */
void PyLauncher::invoke_method_async(
		IApiMethodSP								method,
		IParamValVectorSP							params,
		const std::function<void (IParamValSP)>		&completion) {

}

/**
 * Invokes a method and returns the return value
 */
IParamValSP PyLauncher::invoke_method(
		IApiMethodSP								method,
		IParamValVectorSP							params) {

	InvokeMethodMsgSP  msg = std::make_shared<InvokeMethodMsg>(
			-1,
			0,
			0,
			std::dynamic_pointer_cast<JsonParamValVectorBase>(params));

	int32_t id = m_transport->send(
			"invoke-method",
			msg);

	// TODO: wait for response with id=='id'
	fprintf(stdout, "TODO: wait for response id=%d\n", id);

	// TODO: placeholder
	JsonParamValIntSP ret = std::make_shared<JsonParamValInt>(0);

	return std::dynamic_pointer_cast<IParamVal>(ret);
}

std::string PyLauncher::find_python() {
	// Search through the path to find Python
	const char *sp = getenv("PATH");
	std::string python;

	while (sp && *sp) {
		const char *np = strchr(sp, PS);
		char *path;

		if (np) {
			path = (char *)alloca((np-sp)+64);
			memcpy(path, sp, (np-sp));
			path[np-sp] = 0;
			sp = np+1;
		} else {
			path = (char *)alloca(strlen(sp)+64);
			strcpy(path, sp);
			sp = 0;
		}

#ifdef _WIN32
		const char *python_exe[] = {
				"pypy.exe",
				"python3.exe",
				"python.exe",
				0
		};
#else
		const char *python_exe[] = {
				"pypy",
				"python3",
				"python",
				0
		};
#endif
		const char **py_exe_p = python_exe;
		uint32_t init_len = strlen(path);
		while (*py_exe_p) {
			struct stat stat_b;

			path[init_len] = 0;

			strcat(path, "/");
			strcat(path, *py_exe_p);

			fprintf(stdout, "Test: \"%s\"\n", path);

			if (stat(path, &stat_b) == 0 && S_ISREG(stat_b.st_mode)) {
				python = path;
				break;
			}
			py_exe_p++;
		}

		if (python != "") {
			break;
		}
	}

	return python;
}

void PyLauncher::register_methods() {
	m_dispatcher->register_method("initialize-req",
			std::bind(&PyLauncher::initialize_req,this, std::placeholders::_1));
}

void PyLauncher::initialize_req(const nlohmann::json &msg) {
	fprintf(stdout, "initialize_req\n");

	m_received_init = true;

}

void PyLauncher::init_cb(void *ud) {
	fprintf(stdout, "init_cb(ud)\n");
	reinterpret_cast<PyLauncher *>(ud)->init_cb();
}

void PyLauncher::init_cb() {
	fprintf(stdout, "init_cb()\n");

	// Should register statically-registered APIs

	InitializeRspSP rsp = InitializeRsp::mk();
	m_transport->send("init", rsp);
}

} /* namespace tblink */

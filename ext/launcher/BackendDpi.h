/*
 * BackendDpi.h
 *
 *  Created on: Mar 8, 2021
 *      Author: mballance
 */

#pragma once
#include "BackendBase.h"
#include <map>
#include <string>

struct vpi_api_s;
struct t_cb_data;

namespace tblink {

class BackendDpi : public BackendBase {
public:
	BackendDpi(
			struct vpi_api_s 	*vpi_api,
			bool				have_blocking_tasks);

	virtual ~BackendDpi();

	virtual void init(bool (*reschedule)()) override;

	virtual const std::vector<std::string> &args() const override;

	virtual uint64_t simtime() override;

	virtual intptr_t add_simtime_cb(
			uint64_t		delta,
			void 			(*cb_f)(void *),
			void 			*ud) override;

	virtual void remove_simtime_cb(
			intptr_t		id) override;

	void timed_callback(intptr_t id);

	void register_scope(const std::string &key, void *s);

private:
	static int32_t vpi_cb(struct t_cb_data *);

private:
	typedef std::tuple<
			void (*)(void *),
			void *,
			intptr_t> cb_t;
	bool 						(*m_reschedule)();
	void						*m_scope;
	struct vpi_api_s			*m_vpi_api;
	std::vector<std::string>	m_args;
	bool						m_have_blocking_tasks;
	uint32_t					m_cb_id;
	std::map<intptr_t, cb_t>	m_cb_m;
	std::map<std::string, void *>	m_scope_m;

	static BackendDpi			*m_inst;

};

} /* namespace tblink */


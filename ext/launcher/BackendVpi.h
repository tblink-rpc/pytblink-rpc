/*
 * BackendVpi.h
 *
 *  Created on: Mar 12, 2021
 *      Author: mballance
 */
#pragma once
#include <stdint.h>
#include <map>
#include "BackendBase.h"

struct vpi_api_s;
struct t_cb_data;

namespace tblink {

class BackendVpi : public BackendBase {
public:
	BackendVpi(struct vpi_api_s *vpi_api);

	virtual ~BackendVpi();

	virtual void init(const std::function<bool ()>	&reschedule) override;

	virtual const std::vector<std::string> &args() const override;

	virtual uint64_t simtime() override;

	virtual intptr_t add_simtime_cb(
			uint64_t		delta,
			void 			(*cb_f)(void *),
			void 			*ud) override;

	virtual void remove_simtime_cb(
			intptr_t		id) override;

	virtual int32_t get_timeunit() override;

	virtual int32_t get_timeprecision() override;

	void timed_callback(intptr_t id);

	void register_scope(const std::string &key, void *s);

private:
	static int32_t vpi_cb(struct t_cb_data *);

private:
	typedef std::tuple<
			void (*)(void *),
			void *,
			intptr_t> cb_t;

	std::function<bool ()>		m_reschedule;
	struct vpi_api_s			*m_vpi_api;
	std::vector<std::string>	m_args;
	uint32_t					m_cb_id;
	std::map<intptr_t, cb_t>	m_cb_m;

	static BackendVpi			*m_inst;


};

} /* namespace tblink */


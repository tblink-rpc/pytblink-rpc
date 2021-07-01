/*
 * BackendVpi.cpp
 *
 *  Created on: Mar 12, 2021
 *      Author: mballance
 */

#include <string.h>
#include "BackendVpi.h"
#include "vpi_api.h"

namespace tblink {

BackendVpi::BackendVpi(vpi_api_t *vpi_api) :
		m_reschedule(0), m_vpi_api(vpi_api), m_cb_id(0) {
	s_vpi_vlog_info info;

	m_reschedule = 0;

	m_vpi_api->vpi_get_vlog_info(&info);

	for (int32_t i=0; i<info.argc; i++) {
		m_args.push_back(info.argv[i]);
	}

	m_inst = this;
}

BackendVpi::~BackendVpi() {
	// TODO Auto-generated destructor stub
}

void BackendVpi::init(const std::function<bool ()> &reschedule) {
	m_reschedule = reschedule;
}

const std::vector<std::string> &BackendVpi::args() const {
	return m_args;
}

uint64_t BackendVpi::simtime() {
	s_vpi_time t;
	uint64_t ret;

	t.type = vpiSimTime;

	m_vpi_api->vpi_get_time(0, &t);
	ret = t.high;
	ret <<= 32;
	ret |= t.low;

	return ret;
}

intptr_t BackendVpi::add_simtime_cb(
			uint64_t		delta,
			void 			(*cb_f)(void *),
			void 			*ud) {
	intptr_t ret;

	s_cb_data cbd;
	s_vpi_time t;

	t.type = vpiSimTime;
	t.low = delta;
	t.high = (delta >> 32);

	memset(&cbd, 0, sizeof(s_cb_data));
	cbd.cb_rtn = &BackendVpi::vpi_cb;
	cbd.reason = cbAfterDelay;
	cbd.user_data = reinterpret_cast<PLI_BYTE8 *>(m_cb_id);
	ret = m_cb_id;
	m_cb_id++;
	cbd.time = &t;

	vpiHandle h = m_vpi_api->vpi_register_cb(&cbd);
	fprintf(stdout, "add_simtime_cb: %p\n", h);
	fflush(stdout);
	m_cb_m.insert({ret, cb_t(cb_f, ud, reinterpret_cast<intptr_t>(h))});

	return ret;
}

void BackendVpi::remove_simtime_cb(intptr_t	id) {
	// Cancel the callback via DPI
}

int32_t BackendVpi::get_timeunit() {
	return m_vpi_api->vpi_get(vpiTimeUnit, 0);
}

int32_t BackendVpi::get_timeprecision() {
	return m_vpi_api->vpi_get(vpiTimePrecision, 0);
}

void BackendVpi::register_scope(const std::string &key, void *s) {
//	if (m_scope_m.find(key) == m_scope_m.end()) {
//		m_scope_m.insert({key, s});
//	}
}

int32_t BackendVpi::vpi_cb(struct t_cb_data *cbd) {
	fprintf(stdout, "vpi_cb\n");
	fflush(stdout);
	m_inst->timed_callback(reinterpret_cast<intptr_t>(cbd->user_data));
	return 0;
}

// Callback for SV-driven callbacks
void BackendVpi::timed_callback(intptr_t id) {
	std::map<intptr_t,cb_t>::iterator it;

	fprintf(stdout, "timed_callback\n");
	fflush(stdout);

	if ((it=m_cb_m.find(id)) != m_cb_m.end()) {
		std::get<0>(it->second)(std::get<1>(it->second));
		m_cb_m.erase(it);

		if (m_reschedule) {
			if (!m_reschedule()) {
				fprintf(stdout, "Main routine ended\n");
				m_vpi_api->vpi_control(vpiFinish, 1);
			}
		} else {
			fprintf(stdout, "Warning: no reschedule function present\n");
		}
	} else {
		// TODO: warning
		fprintf(stdout, "Warning: callback %d unknown\n", id);
	}
}

BackendVpi *BackendVpi::m_inst = 0;

} /* namespace tblink */

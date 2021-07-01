
#pragma once
#include <functional>
#include <stdint.h>
#include <string>
#include <vector>
#include "IReschedule.h"

namespace tblink {

class IBackend {
public:

	virtual ~IBackend() { }

	virtual void init(const std::function<bool ()> &reschedule) = 0;

	virtual const std::vector<std::string> &args() const = 0;

	virtual uint64_t simtime() = 0;

	virtual intptr_t add_simtime_cb(
			uint64_t		delta,
			void 			(*cb_f)(void *),
			void 			*ud) = 0;

	virtual void remove_simtime_cb(
			intptr_t		id) = 0;

	virtual int32_t get_timeunit() = 0;

	virtual int32_t get_timeprecision() = 0;

};

}


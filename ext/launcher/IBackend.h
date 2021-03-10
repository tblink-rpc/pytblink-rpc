
#pragma once
#include <stdint.h>

class IBackend {
public:

	virtual ~IBackend() { }

	virtual uint64_t simtime() = 0;

	virtual void add_simtime_cb(
			uint64_t		delta,
			void 			(*cb_f)(void *),
			void 			*ud
			) = 0;

};

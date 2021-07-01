/*
 * IReschedule.h
 *
 *  Created on: Mar 11, 2021
 *      Author: mballance
 */

#pragma once

namespace tblink {

class IReschedule {
public:

	virtual ~IReschedule() { }

	virtual bool reschedule() = 0;

};

}


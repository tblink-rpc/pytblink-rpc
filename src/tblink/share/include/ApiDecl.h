/*
 * ApiDef.h
 *
 *  Created on: Apr 3, 2021
 *      Author: mballance
 */
#include <stdio.h>

namespace tblink {

template <class T> class ApiDecl {
public:

	ApiDecl() { };

	T *inst() { return &m_inst; }

private:
	T				m_inst;

};


}

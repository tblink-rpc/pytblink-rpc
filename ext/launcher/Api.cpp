/*
 * Api.cpp
 *
 *  Created on: Apr 6, 2021
 *      Author: mballance
 */

#include "Api.h"
#include "ApiMethod.h"

namespace tblink {

Api::Api(const std::string &id) :
		m_id(id), m_index(-1), m_is_import(false) {
	// TODO Auto-generated constructor stub

}

Api::~Api() {
	// TODO Auto-generated destructor stub
}

IApiMethodSP Api::add_method(const std::string &name) {
	ApiMethodSP ret = std::make_shared<ApiMethod>(name);


	return ret;
}

IApiMethodSP Api::get_method(const std::string &name) {
	std::map<std::string,uint32_t>::const_iterator it;

	if ((it=m_method_m.find(name)) != m_method_m.end()) {
		return m_methods.at(it->second);
	} else {
		// Null
		return IApiMethodSP();
	}
}

} /* namespace tblink */

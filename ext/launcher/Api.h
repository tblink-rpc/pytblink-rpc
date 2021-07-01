/*
 * Api.h
 *
 *  Created on: Apr 6, 2021
 *      Author: mballance
 */

#pragma once
#include <vector>
#include <map>
#include "IApi.h"
#include "ApiMethod.h"

namespace tblink {

class Api;
typedef std::shared_ptr<Api> ApiSP;
class Api : public IApi {
public:
	Api(const std::string &id);

	virtual ~Api();

	virtual const std::string &id() const override {
		return m_id;
	}

	int32_t index() const { return m_index; }

	void index(int32_t i) { m_index = i; }

	virtual const bool is_import() const override {
		return m_is_import;
	}

	virtual void is_import(bool v) {
		m_is_import = v;
	}

	virtual IApiMethodSP add_method(const std::string &name) override;

	virtual IApiMethodSP get_method(const std::string &name) override;

private:
	std::string							m_id;
	int32_t								m_index;
	bool								m_is_import;
	std::vector<ApiMethodSP>			m_methods;
	std::map<std::string,uint32_t>		m_method_m;

};

} /* namespace tblink */


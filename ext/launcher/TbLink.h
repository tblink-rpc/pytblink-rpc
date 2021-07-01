/*
 * TbLink.h
 *
 *  Created on: Apr 1, 2021
 *      Author: mballance
 */

#pragma once
#include <map>
#include <memory>
#include <string>
#include <vector>
#include "Api.h"
#include "ITbLink.h"
#include "IEndpoint.h"

namespace tblink {

class TbLink : public ITbLink {
public:
	TbLink();

	virtual ~TbLink();

	virtual IPyLauncher *createLauncher(IBackend *backend) override;

	virtual IApiSP mkApi(const std::string &id) override;

	virtual IApiBundleSP mkApiBundle(const std::string &id) override;

	virtual void add_export(
			IApiSP 			api,
			IApiExportSP	impl) override;

	virtual void add_import(IApiSP api) override;

	virtual IApiSP get_import(const std::string &id) override;

	virtual void add_bundle(IApiBundleSP bundle) override;

	virtual IEndpoint *get_default_endpoint() const override;

//	virtual IParamValVectorSP mkParamValVector(
//			int32_t				size_hint=-1) override;
//
//	virtual IParamValIntSP mkParamValInt(
//			uint64_t			val,
//			bool				is_signed,
//			int32_t				width=-1) override;

	static TbLink *inst();

private:
	static std::unique_ptr<TbLink>		m_inst;
	std::vector<ApiSP>					m_imports;
	std::map<std::string,uint32_t>		m_import_m;
	std::vector<ApiSP>					m_exports;
	std::vector<IApiExportSP>			m_export_impl;
	std::map<std::string,uint32_t>		m_export_m;

	std::vector<IEndpoint *>			m_endpoints;
};

} /* namespace tblink */


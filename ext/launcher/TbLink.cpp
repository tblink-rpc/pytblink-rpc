/*
 * TbLink.cpp
 *
 *  Created on: Apr 1, 2021
 *      Author: mballance
 */

#include "TbLink.h"
#include "PyLauncher.h"

namespace tblink {

TbLink::TbLink() {
	// TODO Auto-generated constructor stub

}

TbLink::~TbLink() {
	// TODO Auto-generated destructor stub
}

IPyLauncher *TbLink::createLauncher(IBackend *backend) {
	IPyLauncher *ret = new PyLauncher(backend);
	m_endpoints.push_back(ret);

	return ret;
}

IApiSP TbLink::mkApi(const std::string &id) {
	return std::make_shared<Api>(id);
}

IApiBundleSP TbLink::mkApiBundle(const std::string &id) {

}

void TbLink::add_export(
		IApiSP 			api,
		IApiExportSP	impl) {
	ApiSP api_i = std::dynamic_pointer_cast<Api>(api);

	api_i->is_import(false);
	api_i->index(m_exports.size());
	m_export_m.insert({api->id(), m_exports.size()});
	m_exports.push_back(api_i);
	m_export_impl.push_back(impl);
}

void TbLink::add_import(IApiSP api) {
	ApiSP api_i = std::dynamic_pointer_cast<Api>(api);

	api_i->is_import(true);
	api_i->index(m_imports.size());
	m_import_m.insert({api->id(), m_imports.size()});
	m_imports.push_back(api_i);
}

IApiSP TbLink::get_import(const std::string &id) {
	std::map<std::string,uint32_t>::const_iterator it;

	if ((it=m_import_m.find(id)) != m_import_m.end()) {
		return m_imports.at(it->second);
	} else {
		return IApiSP();
	}
}

void TbLink::add_bundle(IApiBundleSP bundle) {

}

IEndpoint *TbLink::get_default_endpoint() const {
	return m_endpoints.at(0);
}

//IParamValVectorSP TbLink::mkParamValVector(
//		int32_t				size_hint) {
//
//}
//
//IParamValIntSP TbLink::mkParamValInt(
//		uint64_t			val,
//		bool				is_signed,
//		int32_t				width) {
//	;
//}

TbLink *TbLink::inst() {
	if (!m_inst) {
		m_inst = std::unique_ptr<TbLink>(new TbLink());
	}

	return m_inst.get();
}


std::unique_ptr<TbLink>	TbLink::m_inst;

} /* namespace tblink */

/**
 * Used to get a handle to the TbLink singleton
 */
extern "C" tblink::ITbLink *get_tblink_inst() {
	return tblink::TbLink::inst();
}


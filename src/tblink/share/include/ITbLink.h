/*
 * ITbLink.h
 *
 *  Created on: Apr 1, 2021
 *      Author: mballance
 */

#pragma once
#include "IPyLauncher.h"
#include "IApi.h"
#include "IApiBundle.h"
#include "IApiExport.h"
#include "IBackend.h"
#include "IParamVal.h"
#include "IParamValInt.h"
#include "IParamValVector.h"

namespace tblink {

class ITbLink {
public:

	virtual ~ITbLink() { }

	virtual IPyLauncher *createLauncher(IBackend *backend) = 0;

	virtual IApiSP mkApi(const std::string &id) = 0;

	virtual IApiBundleSP mkApiBundle(const std::string &id) = 0;

	virtual void add_export(
			IApiSP 			api,
			IApiExportSP	impl) = 0;

	virtual void add_import(IApiSP api) = 0;

	virtual IApiSP get_import(const std::string &id) = 0;

	virtual void add_bundle(IApiBundleSP bundle) = 0;

	virtual IEndpoint *get_default_endpoint() const = 0;

//	virtual IParamValVectorSP mkParamValVector(
//			int32_t				size_hint=-1) = 0;
//
//	virtual IParamValIntSP mkParamValInt(
//			uint64_t			val,
//			bool				is_signed,
//			int32_t				width=-1) = 0;


};

}



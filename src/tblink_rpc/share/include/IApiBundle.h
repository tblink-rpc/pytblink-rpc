/*
 * IApiBundle.h
 *
 *  Created on: Apr 4, 2021
 *      Author: mballance
 */

#pragma once
#include "IApi.h"
#include "IApiExport.h"

namespace tblink {

class IApiBundle;
typedef std::shared_ptr<IApiBundle> IApiBundleSP;
class IApiBundle {
public:

	virtual ~IApiBundle() { }

	virtual void add_export(
			IApiSP 			api,
			IApiExportSP	impl) = 0;

	virtual void add_import(IApiSP api) = 0;

};

}


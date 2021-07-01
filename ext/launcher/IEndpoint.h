/*
 * IEndpoint.h
 *
 *  Created on: Apr 3, 2021
 *      Author: mballance
 */

#pragma once
#include <functional>
#include <stdint.h>
#include <vector>
#include "IApi.h"
#include "IApiExport.h"
#include "IParamVal.h"
#include "IParamValInt.h"
#include "IParamValStr.h"
#include "IParamValVector.h"

namespace tblink {

class IEndpoint {
public:

	virtual ~IEndpoint() { }

	/**
	 * Phasing-control methods
	 */

	// Note, likely need blocking and non-blocking endpoints

	/**
	 * Notify that build in this environment is complete
	 */
	virtual bool build_complete() = 0;

	/**
	 * Notify that connect in this environment is complete
	 */
	virtual bool connect_complete() = 0;

	/**
	 * Registers an API expected to be implemented
	 * by the connected environment
	 */
	virtual void add_import(IApiSP api) = 0;

	/**
	 * Registers an API that this environment implements
	 */
	virtual void add_export(
			IApiSP 				api,
			IApiExportSP		impl) = 0;

	virtual void set_export_impl(
			IApiSP 				api,
			IApiExportSP		impl) = 0;

	virtual IParamValVectorSP mkParamValVector() = 0;

	virtual IParamValIntSP mkParamValInt(
			uint64_t			val,
			bool				is_signed,
			int32_t				width=-1) = 0;

	virtual IParamValStrSP mkParamValStr(const std::string &v) = 0;

	/**
	 * Invokes a method, calling the completion function when
	 * the call is complete
	 */
	virtual void invoke_method_async(
			IApiMethodSP								method,
			IParamValVectorSP							params,
			const std::function<void (IParamValSP)>		&completion) = 0;

	/**
	 * Invokes a method and returns the return value
	 */
	virtual IParamValSP invoke_method(
			IApiMethodSP								method,
			IParamValVectorSP							params) = 0;

};


}


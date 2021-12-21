/*
 * IApiExport.h
 *
 *  Created on: Apr 4, 2021
 *      Author: mballance
 */

#pragma once
#include "IParamVal.h"
#include "IParamValVector.h"

namespace tblink {

class IApiExport;
typedef std::shared_ptr<IApiExport> IApiExportSP;

/**
 * Implementation for an API being exported
 * from this environment
 */
class IApiExport {
public:

	virtual ~IApiExport() {  }

	/**
	 * Export implementation must provide 'invoke'
	 */
	virtual IParamValSP invoke(
			int32_t				method_id,
			IParamValVectorSP	params) = 0;

};

}

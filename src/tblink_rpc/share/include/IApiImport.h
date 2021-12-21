/*
 * IApiImport.h
 *
 *  Created on: Apr 4, 2021
 *      Author: mballance
 */

#pragma once
#include "IApi.h"
#include "IApiMethod.h"

namespace tblink {

class IApiImport;
typedef std::shared_ptr<IApiImport> IApiImportSP;
class IApiImport : public virtual IApi {
public:

	virtual ~IApiImport() { }

};

}

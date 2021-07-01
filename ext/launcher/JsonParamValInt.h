/*
 * ValInt.h
 *
 *  Created on: Oct 1, 2020
 *      Author: ballance
 */

#pragma once
#include "IParamValInt.h"
#include "JsonParamVal.h"

namespace tblink {

class JsonParamValInt;
typedef std::shared_ptr<JsonParamValInt> JsonParamValIntSP;
class JsonParamValInt : public JsonParamVal, public virtual IParamValInt {
public:
	JsonParamValInt(int64_t v);

	JsonParamValInt(const nlohmann::json &msg);

	virtual ~JsonParamValInt();

	int64_t val() const { return m_val; }

	void val(int64_t v) { m_val = v; }

	virtual uint64_t val_u() { return m_val; }

	virtual int64_t val_s() { return m_val; }

	virtual nlohmann::json dump() override;

	static JsonParamValIntSP mk(const nlohmann::json &msg);

	static JsonParamValIntSP mk(int32_t v);

private:
	int64_t					m_val;

};

} /* namespace tblink */


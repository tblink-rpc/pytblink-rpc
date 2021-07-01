/*
 * ValVector.h
 *
 *  Created on: Oct 1, 2020
 *      Author: ballance
 */

#pragma once
#include <functional>

#include "JsonParamVal.h"
#include "IParamValVector.h"

namespace tblink {

class JsonParamValVectorBase;
typedef std::shared_ptr<JsonParamValVectorBase> JsonParamValVectorBaseSP;
class JsonParamValVectorBase : public JsonParamVal, public virtual IParamValVector {
public:
	JsonParamValVectorBase();

	JsonParamValVectorBase(
			std::function<JsonParamValSP(const nlohmann::json &)> 	ctor,
			const nlohmann::json 							&msg);

	virtual ~JsonParamValVectorBase();

	virtual uint32_t size() override { return m_children.size(); }

	virtual IParamValSP at(uint32_t idx) override { return m_children.at(idx); }

	virtual void push_back(IParamValSP v) override;

	const std::vector<JsonParamValSP> &children() const {
		return m_children;
	}

	JsonParamValSP children(uint32_t idx) const {
		return m_children.at(idx);
	}

	virtual nlohmann::json dump();

	static JsonParamValVectorBaseSP mk(
			std::function<JsonParamValSP(const nlohmann::json &)> 	ctor,
			const nlohmann::json 							&msg);

private:
	std::vector<JsonParamValSP>				m_children;

};


} /* namespace tblink */


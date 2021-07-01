/*
 * ValVector.h
 *
 *  Created on: Oct 1, 2020
 *      Author: ballance
 */

#pragma once
#include "JsonParamValVectorBase.h"

namespace tblink {

template <class T> class JsonParamValVector : public JsonParamValVectorBase {
public:
	typedef std::shared_ptr<JsonParamValVector<T>> SP;
public:

	JsonParamValVector() { }

	const std::vector<std::shared_ptr<T>> &children() const {
		return std::dynamic_pointer_cast<std::vector<std::shared_ptr<T>>>(
				JsonParamValVectorBase::children());
	}

	std::shared_ptr<T> children(uint32_t idx) const {
		return std::dynamic_pointer_cast<std::shared_ptr<T>>(
				JsonParamValVectorBase::children(idx));
	}

	static SP mk(const nlohmann::json &msg) {
		return std::dynamic_pointer_cast<JsonParamValVector<T>>(
				JsonParamValVectorBase::mk(
						[&](const nlohmann::json &sm) {
							return JsonParamValSP(new T(sm));
						}, msg));
	}

	static JsonParamValVector<T> *mk() {
		return new JsonParamValVector<T>();
	}

};

}


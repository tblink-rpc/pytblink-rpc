/*
 * vpi_api.cpp
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *  http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 *
 *  Created on: Mar 10, 2021
 *      Author: mballance
 *
 *  Provides a dynamic loader for the VPI API
 */

#include "vpi_api.h"
#ifndef _WIN32
#include <dlfcn.h>
#endif
#include <stdio.h>

struct vpi_api_func_s {
	const char *name;
	void **fptr;
};

static bool prv_vpi_api_tryload = false;
static bool prv_vpi_api_loaded = false;
static vpi_api_s prv_vpi_api;
static char prv_vpi_api_buf[256];

static void *find_vpi_lib() {
	void *vpi_lib = dlopen(0, RTLD_LAZY);

	if (!vpi_lib) {
		snprintf(prv_vpi_api_buf, sizeof(prv_vpi_api_buf),
				"Failed to locate VPI library: %s", dlerror());
	}

	return vpi_lib;
}


static vpi_api_func_s api_tab[] = {
		{"vpi_control", (void **)&prv_vpi_api.vpi_control},
		{"vpi_get_value", (void **)&prv_vpi_api.vpi_get_value},
		{"vpi_put_value", (void **)&prv_vpi_api.vpi_put_value},
		{"vpi_handle", (void **)&prv_vpi_api.vpi_handle},
		{"vpi_iterate", (void **)&prv_vpi_api.vpi_iterate},
		{"vpi_register_cb", (void **)&prv_vpi_api.vpi_register_cb},
		{"vpi_remove_cb",   (void **)&prv_vpi_api.vpi_remove_cb},
		{"vpi_scan", (void **)&prv_vpi_api.vpi_scan},
		{"vpi_free_object", (void **)&prv_vpi_api.vpi_free_object},
		{"vpi_get", (void **)&prv_vpi_api.vpi_get},
		{"vpi_get_vlog_info", (void **)&prv_vpi_api.vpi_get_vlog_info},
		{"vpi_get_str", (void **)&prv_vpi_api.vpi_get_str},
		{"vpi_get_time", (void **)&prv_vpi_api.vpi_get_time},
		{"vpi_register_systf", (void **)&prv_vpi_api.vpi_register_systf},
		{0, 0}
};

static bool load_vpi_api() {
	if (prv_vpi_api_tryload) {
		return prv_vpi_api_loaded;
	}

	// Only try to load the VPI API once
	prv_vpi_api_tryload = true;

	void *vpi_lib = find_vpi_lib();
	if (!vpi_lib) {
		return false;
	}

	for (uint32_t i=0; api_tab[i].name; i++) {
		void *val = dlsym(vpi_lib, api_tab[i].name);
		if (!val) {
			snprintf(prv_vpi_api_buf, sizeof(prv_vpi_api_buf),
					"Failed to find VPI symbol \"%s\" (%s)",
					api_tab[i].name, dlerror());
			return false;
		}
		(*api_tab[i].fptr) = val;
	}

	prv_vpi_api_loaded = true;
	return prv_vpi_api_loaded;
}

vpi_api_t *get_vpi_api() {
	if (!prv_vpi_api_tryload) {
		prv_vpi_api_loaded = load_vpi_api();
		prv_vpi_api_tryload = true;
	}

	if (prv_vpi_api_loaded) {
		return &prv_vpi_api;
	} else {
		return 0;
	}
}

const char *get_vpi_api_error() {
	return prv_vpi_api_buf;
}



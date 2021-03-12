/*
 * vpi_api.h
 *
 *  Created on: Mar 10, 2021
 *      Author: mballance
 */

#pragma once
#include "vpi_user.h"

typedef struct vpi_api_s {
	void (*vpi_get_value)(vpiHandle, p_vpi_value);
	PLI_INT32 (*vpi_control)(PLI_INT32, ...);
	vpiHandle (*vpi_put_value)(vpiHandle, p_vpi_value, p_vpi_time, PLI_INT32);
	vpiHandle (*vpi_handle)(PLI_INT32, vpiHandle);
	vpiHandle (*vpi_iterate)(PLI_INT32, vpiHandle);
	vpiHandle (*vpi_register_cb)(p_cb_data);
	PLI_INT32 (*vpi_remove_cb)(vpiHandle);
	vpiHandle (*vpi_scan)(vpiHandle);
	PLI_INT32 (*vpi_free_object)(vpiHandle);
	PLI_INT32 (*vpi_get)(PLI_INT32, vpiHandle);
	PLI_INT32 (*vpi_get_vlog_info)(p_vpi_vlog_info);
	PLI_BYTE8 *(*vpi_get_str)(PLI_INT32, vpiHandle);
	void      (*vpi_get_time)(vpiHandle, p_vpi_time);
	vpiHandle (*vpi_register_systf)(p_vpi_systf_data);
} vpi_api_t;

vpi_api_t *get_vpi_api();

/**
 * Returns an error message when the API fails to load
 */
const char *get_vpi_api_error();





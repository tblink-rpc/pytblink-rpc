/*
 * tblink.h
 *
 *  Created on: Apr 1, 2021
 *      Author: mballance
 */

#pragma once
#include "ITbLink.h"

#ifndef _WIN32
#include <dlfcn.h>
#else
#error Windows not supported yet
#endif
#include <stdlib.h>

static tblink::ITbLink *load_tblink();

/**
 * load_tblink()
 *
 * Load the TbLink library and return an instance
 */
static tblink::ITbLink *load_tblink() {
	static tblink::ITbLink *inst = 0;

	if (!inst) {
		const char *tblink_lib = getenv("TBLINK_LIB");

		if (tblink_lib && tblink_lib[0]) {
			// Load this file
			void *libh = dlopen(tblink_lib, RTLD_LAZY);

			if (!libh) {
				fprintf(stdout, "Error: Failed to load tblink library \"%s\" %s\n",
						tblink_lib,
						dlerror());
				exit(1);
			}

			void *sym = dlsym(libh, "get_tblink_inst");

			if (!sym) {
				fprintf(stdout, "Error: Failed to find get_tblink_inst in library \"%s\"\n", tblink_lib);
				exit(1);
			}

			inst = ((tblink::ITbLink *(*)())sym)();
		} else {
			// Search
		}

	}

	return inst;
}




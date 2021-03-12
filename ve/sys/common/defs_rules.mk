
TBLINK_VE_COMMONDIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
TBLINK_DIR := $(abspath $(TBLINK_VE_COMMONDIR)/../../..)
PACKAGES_DIR := $(TBLINK_DIR)/packages
DV_MK := $(shell PATH=$(PACKAGES_DIR)/python/bin:$(PATH) python3 -m mkdv mkfile)
#T := $(shell PYTHONPATH=$(TBLINK_DIR)/src:$(PYTHONPATH) python3 -m tblink lib > out)
ENV=PYTHONPATH=$(TBLINK_DIR)/src:$(PYTHONPATH) PATH=$(PACKAGES_DIR)/python/bin:$(PATH)
T := $(shell $(ENV) env > out)

#PYTHONPATH:=$(TBLINK_DIR)/src:$(PYTHONPATH)
#export PYTHONPATH

MKDV_PYTHONPATH += $(TBLINK_VE_COMMONDIR)/python
MKDV_PYTHONPATH += $(TBLINK_DIR)/src


ifneq (1,$(RULES))

ifeq (vlsim,$(MKDV_TOOL))
MKDV_VL_SRCS += $(shell $(ENV) python3 -m tblink files)
DPI_LIBS += $(shell $(ENV) python3 -m tblink lib)
endif

ifeq (questa,$(MKDV_TOOL))
MKDV_VL_SRCS += $(shell $(ENV) python3 -m tblink files)
DPI_LIBS += $(shell $(ENV) python3 -m tblink lib)
MKDV_VL_TOP_MODULES += tblink
endif

include $(DV_MK)
else # Rules

include $(DV_MK)
endif

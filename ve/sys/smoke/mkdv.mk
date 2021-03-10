
MKDV_MK:=$(abspath $(lastword $(MAKEFILE_LIST)))
TEST_DIR := $(dir $(MKDV_MK))

MKDV_TOOL ?= vlsim

TOP_MODULE = smoke_tb
MKDV_VL_SRCS += $(TEST_DIR)/smoke_tb.sv
COCOTB_MODULE ?= tblink_tests.smoke
MODULE = $(COCOTB_MODULE)
export MODULE

VLSIM_CLKSPEC += clock=10ns
VLSIM_OPTIONS += -Wno-fatal

include $(TEST_DIR)/../common/defs_rules.mk
RULES := 1

include $(TEST_DIR)/../common/defs_rules.mk

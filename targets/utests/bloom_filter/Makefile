###############################################################################
#
# 
#
###############################################################################

include ../../../init.mk
MODULE := bloom_filter_utest
TEST_MODULE := bloom_filter
DEPENDMODULES := AIM
GLOBAL_CFLAGS += -DAIM_CONFIG_INCLUDE_MODULES_INIT=1
GLOBAL_CFLAGS += -DAIM_CONFIG_INCLUDE_MAIN=1
include $(BUILDER)/build-unit-test.mk

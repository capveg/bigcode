###############################################################################
#
# 
#
###############################################################################

LIBRARY := snmp_subagent
$(LIBRARY)_SUBDIR := $(dir $(lastword $(MAKEFILE_LIST)))
include $(BUILDER)/lib.mk

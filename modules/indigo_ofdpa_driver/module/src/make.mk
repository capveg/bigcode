###############################################################################
#
# 
#
###############################################################################

LIBRARY := indigo_ofdpa_driver
$(LIBRARY)_SUBDIR := $(dir $(lastword $(MAKEFILE_LIST)))
include $(BUILDER)/lib.mk

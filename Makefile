################################################################################
# Makefile for AWS - amazon web services task
################################################################################

# Prefer bash shell
export SHELL=/bin/bash

## Define repositories dependencies paths

## Make sure of current python path
export PYTHONPATH=$(pwd):./

self := $(abspath $(lastword $(MAKEFILE_LIST)))
parent := $(dir $(self))

ifneq (,$(VERBOSE))
    override VERBOSE:=
else
    override VERBOSE:=@
endif

.PHONY: test
test:
	$(VERBOSE) source .bashrc
	$(VERBOSE) nosetests ./tests
.PHONY: test_api
test_api:
	$(VERBOSE) source .bashrc
	$(VERBOSE) nosetests api/test/test_aws_api.py
.PHONY: smoke
smoke:
	$(VERBOSE) nosetests ./
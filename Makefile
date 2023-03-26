SHELL=/bin/bash

.DEFAULT_GOAL := _help

# NOTE: must put a <TAB> character and two pound "\t##" to show up in this list.  Keep it brief! IGNORE_ME
.PHONY: _help
_help:
	@grep -h "##" $(MAKEFILE_LIST) | grep -v IGNORE_ME | sed -e 's/##//' | column -t -s $$'\t'



# ---------------------------------------
# init & venv
# ---------------------------------------

.PHONY: init
init:	## Set up a Python virtual environment
	git submodule update --init
	$(PY_SYS_INTERPRETER) -m venv --clear .venv
	- if [ -z "$(CI)" ]; then $(PY_SYS_INTERPRETER) -m venv --upgrade-deps .venv; fi
	- direnv allow || echo -e "\r\nHINT: run 'source .venv/bin/activate', and 'make deps'"

# include .env
SKIP_VENV ?=
PYTHON ?= $(shell which python)
PWD ?= $(shell pwd)
.PHONY: _venv
_venv:
	# Test to enforce venv usage across important make targets
	[ "$(SKIP_VENV)" ] || [ "$(PYTHON)" = "$(PWD)/.venv/bin/python" ] || [ "$(PYTHON)" = "$(PWD)/.venv/Scripts/python" ]



# ---------------------------------------
# Install requirements
# ---------------------------------------

PY_SYS_INTERPRETER ?=
ifeq ($(PY_SYS_INTERPRETER),)
	ifeq ($(OS),Windows_NT)
		PY_SYS_INTERPRETER += python3
	else
		PY_SYS_INTERPRETER += /usr/bin/python3
	endif
endif

PIP ?= $(PYTHON) -m pip

REQ_OPT := requirements-optional.txt
REQ_LINT := requirements-lint.txt
REQ_TEST := requirements-test.txt
REQ_TEST_OLD := requirements-test-old.txt

PIP_OPT_ARGS ?=

.PHONY: deps
deps: _venv	## Install requirements
	$(PIP) install --user wheel
	$(PIP) install --user $(PIP_OPT_ARGS) -r requirements.txt
	- $(PIP) install --user $(PIP_OPT_ARGS) -r $(REQ_OPT)
	- $(PIP) install --user $(PIP_OPT_ARGS) -r $(REQ_LINT)
	- $(PIP) install --user $(PIP_OPT_ARGS) -r $(REQ_TEST) || \
	    $(PIP) install --user $(PIP_OPT_ARGS) -r $(REQ_TEST_OLD) || \
	    echo "TEST REQs failed. Are you on a very old computer?"


# ---------------------------------------
# Format, lint, test
# ---------------------------------------

.PHONY: format
format: _venv	## Format with isort & black
	if [ "$(CHANGED_FILES_PY_FLAG)" = 1 ]; then isort $(CHANGED_FILES_PY) ; fi
	if [ "$(CHANGED_FILES_PY_FLAG)" = 1 ]; then black $(CHANGED_FILES_PY) ; fi


LINT_LOCS := ntclient/ tests/ setup.py
CHANGED_FILES_RST ?= $(shell git diff origin/master --name-only --diff-filter=MACRU \*.rst)
CHANGED_FILES_PY ?= $(shell git diff origin/master --name-only --diff-filter=MACRU \*.py)
CHANGED_FILES_PY_FLAG ?= $(shell if [ "$(CHANGED_FILES_PY)" ]; then echo 1; else echo 0; fi)

.PHONY: lint
lint: _venv	## Lint code and documentation
	# lint RST
	if [ "$(CHANGED_FILES_RST)" ]; then doc8 --quiet $(CHANGED_FILES_RST); fi
	# check formatting: Python
	if [ "$(CHANGED_FILES_PY_FLAG)" = 1 ]; then isort --diff --check $(CHANGED_FILES_PY) ; fi
	if [ "$(CHANGED_FILES_PY_FLAG)" = 1 ]; then black --check $(CHANGED_FILES_PY) ; fi
	# lint Python
	if [ "$(CHANGED_FILES_PY_FLAG)" = 1 ]; then pycodestyle --statistics $(CHANGED_FILES_PY); fi
	if [ "$(CHANGED_FILES_PY_FLAG)" = 1 ]; then bandit -q -c .banditrc -r $(CHANGED_FILES_PY); fi
	if [ "$(CHANGED_FILES_PY_FLAG)" = 1 ]; then flake8 $(CHANGED_FILES_PY); fi
	if [ "$(CHANGED_FILES_PY_FLAG)" = 1 ]; then mypy $(CHANGED_FILES_PY); fi
	if [ "$(CHANGED_FILES_PY_FLAG)" = 1 ]; then pylint $(CHANGED_FILES_PY); fi


TEST_HOME := tests/
MIN_COV := 80
.PHONY: test
.PHONY: test
test: _venv	## Run CLI unittests
	coverage run -m pytest $(TEST_HOME)
	coverage report



# ---------------------------------------
# SQLite submodule: nt-sqlite
# ---------------------------------------

# TODO: why does this still work? Is this what `ntserv.ntdb.sql` should do?

.PHONY: ntsqlite/build
ntsqlite/build:
	$(PY_SYS_INTERPRETER) ntclient/ntsqlite/sql/__init__.py

# TODO: nt-sqlite/test



# ---------------------------------------
# Python build & install
# ---------------------------------------

.PHONY: _build
_build:
	$(PY_SYS_INTERPRETER) setup.py --quiet sdist

.PHONY: build
build:	## Create sdist binary *.tar.gz
build: _build clean


.PHONY: install
install:	## pip install .
	$(PY_SYS_INTERPRETER) -m pip install wheel
	$(PY_SYS_INTERPRETER) -m pip install . || $(PY_SYS_INTERPRETER) -m pip install --user .
	$(PY_SYS_INTERPRETER) -m pip show nutra
	- $(PY_SYS_INTERPRETER) -c 'import shutil; print(shutil.which("nutra"));'
	nutra -v



# ---------------------------------------
# Clean
# ---------------------------------------

RECURSIVE_CLEAN_LOCS ?= $(shell find ntclient/ tests/ \
-name __pycache__ \
-o -name .coverage \
-o -name .mypy_cache \
-o -name .pytest_cache)

.PHONY: clean
clean:	## Clean up __pycache__ and leftover bits
	rm -f .coverage ntclient/ntsqlite/sql/nt.sqlite3
	rm -rf build/
	rm -rf nutra.egg-info/
	rm -rf .pytest_cache/ .mypy_cache/
	# Recursively find & remove
	if [ "$(RECURSIVE_CLEAN_LOCS)" ]; then rm -rf $(RECURSIVE_CLEAN_LOCS); fi



# ---------------------------------------
# Extras
# ---------------------------------------

CLOC_ARGS ?=
.PHONY: extras/cloc
extras/cloc:	## Count lines of source code
	- cloc HEAD

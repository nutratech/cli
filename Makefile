SHELL=/bin/bash

.DEFAULT_GOAL := _help

# NOTE: must put a <TAB> character and two pound "\t##" to show up in this list.  Keep it brief! IGNORE_ME
.PHONY: _help
_help:
	@printf "\nUsage: make <command>, valid commands:\n\n"
	@grep "##" $(MAKEFILE_LIST) | grep -v ^# | grep -v IGNORE_ME | sed -e 's/##//' | column -t -s $$'\t'



# ---------------------------------------
# init & venv
# ---------------------------------------

.PHONY: init
init:	## Set up a Python virtual environment
	# Fetch submodule
	git submodule update --init
	# Re-add virtual environment
	rm -rf .venv
	${PY_SYS_INTERPRETER} -m venv .venv
	# Upgrade dependencies and pip, if NOT running in CI automation
	- if [ -z "${CI}" ]; then ${PY_SYS_INTERPRETER} -m venv --upgrade-deps .venv; fi
	direnv allow
	@echo "INFO: Successfully initialized venv, run 'make deps' now!"

# include .env
SKIP_VENV ?=
PYTHON ?= $(shell which python)
PWD ?= $(shell pwd)
.PHONY: _venv
_venv:
	# Test to enforce venv usage across important make targets
	test "${SKIP_VENV}" || test "${PYTHON}" = "${PWD}/.venv/bin/python"
	@echo "OK"



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

PY_VIRTUAL_INTERPRETER ?= python
PIP ?= $(PY_VIRTUAL_INTERPRETER) -m pip

REQ_OPT := requirements-optional.txt
REQ_LINT := requirements-lint.txt
REQ_TEST := requirements-test.txt
REQ_TEST_OLD := requirements-test-old.txt

# TODO: this is a fragile hack (to get it to work in CI and locally too)
PIP_OPT_ARGS ?= $(shell if [ "$(SKIP_VENV)" ]; then echo "--user"; fi)

.PHONY: deps
deps: _venv	## Install requirements
	# Install requirements
	${PIP} install wheel
	${PIP} install ${PIP_OPT_ARGS} -r requirements.txt
	- ${PIP} install ${PIP_OPT_ARGS} -r ${REQ_OPT}
	- ${PIP} install ${PIP_OPT_ARGS} -r ${REQ_LINT}
	${PIP} install ${PIP_OPT_ARGS} -r ${REQ_TEST} || ${PIP} install ${PIP_OPT_ARGS} -r ${REQ_TEST_OLD}


# ---------------------------------------
# Format, lint, test
# ---------------------------------------

.PHONY: format
format: _venv	## Format with isort & black
ifneq ($(CHANGED_FILES_PY),)
	isort ${CHANGED_FILES_PY}
	black ${CHANGED_FILES_PY}
else
	$(info No changed Python files, skipping.)
endif


# LINT_LOCS := ntclient/ tests/ setup.py
CHANGED_FILES_RST ?= $(shell git diff origin/master --name-only --diff-filter=MACRU \*.rst)
CHANGED_FILES_PY ?= $(shell git diff origin/master --name-only --diff-filter=MACRU \*.py)

.PHONY: lint
lint: _venv	## Lint code and documentation
ifneq ($(CHANGED_FILES_RST),)
	# lint RST
	doc8 --quiet ${CHANGED_FILES_RST}
	@echo "OK"
else
	$(info No changed RST files, skipping.)
endif
ifneq ($(CHANGED_FILES_PY),)
	# check formatting: Python
	isort --diff --check ${CHANGED_FILES_PY}
	black --check ${CHANGED_FILES_PY}
	# lint Python
	pycodestyle --statistics ${CHANGED_FILES_PY}
	bandit -q -c .banditrc -r ${CHANGED_FILES_PY}
	flake8 ${CHANGED_FILES_PY}
	mypy ${CHANGED_FILES_PY}
	pylint ${CHANGED_FILES_PY}
	@echo "OK"
else
	$(info No changed Python files, skipping.)
endif

.PHONY: pylint
pylint:
ifneq ($(CHANGED_FILES_PY),)
	pylint ${CHANGED_FILES_PY}
else
	$(info No changed Python files, skipping.)
endif

.PHONY: mypy
mypy:
ifneq ($(CHANGED_FILES_PY),)
	mypy ${CHANGED_FILES_PY}
else
	$(info No changed Python files, skipping.)
endif


.PHONY: test
test: _venv	## Run CLI unit tests
	coverage run
	coverage report
	- grep fail_under setup.cfg



# ---------------------------------------
# SQLite submodule: nt-sqlite
# ---------------------------------------

# TODO: why does this still work? Is this what `ntserv.ntdb.sql` should do?

.PHONY: ntsqlite/build
ntsqlite/build:
	${PY_SYS_INTERPRETER} ntclient/ntsqlite/sql/__init__.py

# TODO: nt-sqlite/test



# ---------------------------------------
# Python build & install
# ---------------------------------------

.PHONY: _build
_build:
	${PY_SYS_INTERPRETER} setup.py --quiet sdist

.PHONY: build
build:	## Create sdist binary *.tar.gz
build: _build clean


.PHONY: install
install:	## pip install .
	${PY_SYS_INTERPRETER} -m pip install wheel
	${PY_SYS_INTERPRETER} -m pip install . || ${PY_SYS_INTERPRETER} -m pip install --user .
	${PY_SYS_INTERPRETER} -m pip show nutra
	- ${PY_SYS_INTERPRETER} -c 'import shutil; print(shutil.which("nutra"));'
	nutra --version



# ---------------------------------------
# Clean
# ---------------------------------------

RECURSIVE_CLEAN_LOCS ?= $(shell find ntclient/ tests/ \
-name __pycache__ \
-o -name .coverage \
-o -name .mypy_cache \
-o -name .pytest_cache \
)

.PHONY: clean
clean:	## Clean up __pycache__ and leftover bits
	rm -f .coverage ntclient/ntsqlite/sql/nt.sqlite3
	rm -rf build/
	rm -rf nutra.egg-info/
	rm -rf .pytest_cache/ .mypy_cache/
ifneq ($(RECURSIVE_CLEAN_LOCS),)
	# Recursively find & remove
	rm -rf ${RECURSIVE_CLEAN_LOCS}
endif



# ---------------------------------------
# Extras
# ---------------------------------------

.PHONY: extras/cloc
extras/cloc:	## Count lines of source code
	- cloc HEAD ntclient/ntsqlite

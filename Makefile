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
	if [ ! -d .venv ]; then \
		$(PY_SYS_INTERPRETER) -m venv .venv; \
	fi
	- direnv allow
	@echo -e "\r\nNOTE: activate venv, and run 'make deps'\r\n"
	@echo -e "HINT: run 'source .venv/bin/activate'"


PYTHON ?= $(shell which python)
PWD ?= $(shell pwd)
.PHONY: _venv
_venv:
	# Test to enforce venv usage across important make targets
	[ "$(PYTHON)" = "$(PWD)/.venv/bin/python" ] || [ "$(PYTHON)" = "$(PWD)/.venv/Scripts/python" ]


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
REQ_TEST_OLD := requirements-test-win_xp-ubu1604.txt

PIP_OPT_ARGS ?=

.PHONY: _deps
_deps:
	$(PIP) install wheel
	$(PIP) install $(PIP_OPT_ARGS) -r requirements.txt
	- $(PIP) install $(PIP_OPT_ARGS) -r $(REQ_OPT)
	- $(PIP) install $(PIP_OPT_ARGS) -r $(REQ_LINT)
	- $(PIP) install $(PIP_OPT_ARGS) -r $(REQ_TEST) || \
	echo "TEST REQs failed. Try with '--user' flag, or old version: $(PIP) install -r $(REQ_TEST_OLD)"

.PHONY: deps
deps: _venv _deps	## Install requirements


# ---------------------------------------
# Format, lint, test
# ---------------------------------------

.PHONY: format
format:
	isort $(LINT_LOCS)
	autopep8 --recursive --in-place --max-line-length 88 $(LINT_LOCS)
	black $(LINT_LOCS)


LINT_LOCS := ntclient/ tests/ setup.py
YAML_LOCS := ntclient/ntsqlite/.*.yml .github/workflows/ .*.yml
# NOTE: yamllint 	ntclient/ntsqlite/.travis.yml ? (submodule)
# NOTE: doc8 		ntclient/ntsqlite/README.rst  ? (submodule)
.PHONY: _lint
_lint:
	# check formatting: Python
	pycodestyle --max-line-length=99 --statistics $(LINT_LOCS)
	autopep8 --recursive --diff --max-line-length 88 --exit-code $(LINT_LOCS)
	isort --diff --check $(LINT_LOCS)
	black --check $(LINT_LOCS)
	# lint RST (last param is search term, NOT ignore)
	doc8 --quiet *.rst ntclient/ntsqlite/*.rst
	# lint YAML
	yamllint $(YAML_LOCS)
	# lint Python
	bandit -q -c .banditrc -r $(LINT_LOCS)
	mypy $(LINT_LOCS)
	flake8 $(LINT_LOCS)
	pylint $(LINT_LOCS)

.PHONY: lint
lint: _venv _lint	## Lint code and documentation


TEST_HOME := tests/
MIN_COV := 80
.PHONY: _test
_test:
	coverage run -m pytest -v -s -p no:cacheprovider -o log_cli=true $(TEST_HOME)
	coverage report

.PHONY: test
test: _venv _test	## Run CLI unittests


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
install:	## pip install nutra
	$(PY_SYS_INTERPRETER) -m pip install wheel
	$(PY_SYS_INTERPRETER) -m pip install . || $(PY_SYS_INTERPRETER) -m pip install --user .
	$(PY_SYS_INTERPRETER) -m pip show nutra
	- $(PY_SYS_INTERPRETER) -c 'import shutil; print(shutil.which("nutra"));'
	nutra -v


# ---------------------------------------
# Clean
# ---------------------------------------

.PHONY: clean
clean:	## Clean up __pycache__ and leftover bits
	rm -f .coverage ntclient/ntsqlite/sql/nt.sqlite3
	rm -rf build/
	rm -rf nutra.egg-info/
	rm -rf .pytest_cache/ .mypy_cache/
	find ntclient/ tests/ -name __pycache__ -o -name .coverage -o -name .pytest_cache | xargs rm -rf


# ---------------------------------------
# Extras
# ---------------------------------------

CLOC_ARGS ?=
.PHONY: extras/cloc
extras/cloc:	## Count lines of source code
	- cloc \
	--exclude-dir=\
	.venv,venv,\
	.mypy_cache,.pytest_cache,\
	.idea,\
	build,dist \
	--exclude-ext=svg \
	$(CLOC_ARGS) \
	.

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
		/usr/bin/python3 -m venv .venv; \
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

PIP := python -m pip
REQ_OPT := requirements-optional.txt
REQ_LINT := requirements-lint.txt
REQ_TEST := tests/requirements.txt
REQ_OLD := tests/requirements-win_xp-ubu1604.txt
.PHONY: _deps
_deps:
	$(PIP) install wheel
	$(PIP) install -r requirements.txt
	- $(PIP) install -r $(REQ_OPT)
	- $(PIP) install -r $(REQ_LINT)
	- $(PIP) install -r $(REQ_TEST) || (echo "\r\nTEST REQs failed... try old version" && $(PIP) install -r $(REQ_OLD))

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


LINT_LOCS := ntclient/ tests/ scripts/ nutra setup.py
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
	python ntclient/ntsqlite/sql/__init__.py

# TODO: nt-sqlite/test


# ---------------------------------------
# Python build stuff
# ---------------------------------------

.PHONY: _build
_build:
	python setup.py --quiet sdist

.PHONY: build
build: _venv _build clean	## Create sdist binary *.tar.gz

.PHONY: _install
_install:
	python -m pip install wheel
	python -m pip install .
	python -m pip show nutra
	- python -c 'import shutil; print(shutil.which("nutra"));'
	nutra -v

.PHONY: install
install: _venv _install	## pip install nutra

.PHONY: _uninstall
_uninstall:
	python -m pip uninstall -y nutra

.PHONY: uninstall
uninstall: _venv _uninstall	## pip uninstall nutra


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

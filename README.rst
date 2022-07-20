**************
 nutratracker
**************

.. list-table::
  :widths: 15 25 20
  :header-rows: 1

  * -
    -
    -
  * - Test / Linux
    - .. image:: https://github.com/nutratech/cli/actions/workflows/test-linux.yml/badge.svg
        :target: https://github.com/nutratech/cli/actions/workflows/test-linux.yml
        :alt: Test status unknown (Linux)
    -
  * - Test / Windows
    - .. image:: https://github.com/nutratech/cli/actions/workflows/test-win32.yml/badge.svg
        :target: https://github.com/nutratech/cli/actions/workflows/test-win32.yml
        :alt: Test status unknown (Windows)
    -
  * - Other checks
    - .. image:: https://coveralls.io/repos/github/nutratech/cli/badge.svg?branch=master
        :target: https://coveralls.io/github/nutratech/cli?branch=master
        :alt: Coverage unknown
    - .. image:: https://github.com/nutratech/cli/actions/workflows/lint.yml/badge.svg
        :target: https://github.com/nutratech/cli/actions/workflows/lint.yml
        :alt: Lint status unknown
  * - PyPI Release
    - .. image:: https://badgen.net/pypi/v/nutra
        :target: https://pypi.org/project/nutra/
        :alt: Latest version unknown
    - .. image:: https://pepy.tech/badge/nutra/month
        :target: https://pepy.tech/project/nutra
        :alt: Monthly downloads unknown
  * - Supported Runtime
    - .. image:: https://img.shields.io/pypi/pyversions/nutra.svg
        :alt: Python3 (3.4 - 3.10)
    -
  * - Code Style
    - .. image:: https://badgen.net/badge/code%20style/black/000
        :target: https://github.com/ambv/black
        :alt: Code style: black
    -
  * - License
    - .. image:: https://badgen.net/pypi/license/nutra
        :target: https://www.gnu.org/licenses/gpl-3.0.en.html
        :alt: License GPL-3
    -

Command line tools for interacting with government food databases.

*Requires:*

- Python 3.4.0 or later (lzma, ssl & sqlite3 modules) [Win XP / Ubuntu 14.04].
- Packages: see ``setup.py``, and ``requirements.txt`` files.
- Internet connection, to download food database & package dependencies.

See nt database:   https://github.com/nutratech/nt-sqlite

See usda database: https://github.com/nutratech/usda-sqlite

Plugin Development
==================

We're looking to start developing plugins or data modifications sets that
can be imported and built on the base installation, which remains pure.

Notes
=====

On Windows you should check the box during the Python installer
to include ``Scripts`` directory in your ``$PATH``.  This can be done
manually after installation too.

Linux may need to install ``python-dev`` package to build
``python-Levenshtein``.

Windows users may not be able to install ``python-Levenshtein``.

Mac and Linux developers will do well to install ``direnv``.

Main program works 100%, but ``test`` and ``lint`` may break on older operating
systems (Ubuntu 14.04, Windows XP).

Install PyPi release (from pip)
===============================

.. code-block:: bash

  pip install nutra

(**Specify:** flag ``-U`` to upgrade, or ``--pre`` for development releases)

Using the source code directly
==============================
Clone down, initialize ``nt-sqlite`` submodule, and install requirements:

.. code-block:: bash

  git clone https://github.com/nutratech/cli.git
  cd cli
  make init
  # source .venv/bin/activate  # uncomment if NOT using direnv
  make deps

  ./nutra -h

Initialize the DBs (nt and usda).

.. code-block:: bash

  # source .venv/bin/activate  # uncomment if NOT using direnv
  ./nutra init

  # Or install and run as package script
  make install
  nutra init

If installed (or inside ``cli``) folder, the program can also run
with ``python -m ntclient``

Building the PyPi release
#########################

.. code-block:: bash

  # source .venv/bin/activate  # uncomment if NOT using direnv
  make build  # python3 setup.py --quiet sdist
  twine upload dist/nutra-X.X.X.tar.gz

Linting & Tests
===============

Install the dependencies (``make deps``) and then:

.. code-block:: bash

  # source .venv/bin/activate  # uncomment if NOT using direnv
  make format lint test

ArgComplete (tab completion / autocomplete)
===========================================

After installing nutra, argcomplete package should also be installed.

Linux, macOS, and Linux Subsystem for Windows
#############################################

Simply run the following out of a ``bash`` shell. Check their page for more
specifics on using other shells, e.g. ``zsh``, ``fish``, or ``tsh``.

.. code-block:: bash

  activate-global-python-argcomplete

Then you can press tab to fill in or complete subcommands
and to list argument flags.

Windows (Git Bash)
##################

This can work with git bash too. I followed the instructions on their README.

I've run the command to seed the autocomplete script.

.. code-block:: bash

  mkdir -p $HOME/.bash_completion.d
  activate-global-python-argcomplete --user

And my ``~/.bashrc`` file looks like this.

.. code-block:: bash

  export ARGCOMPLETE_USE_TEMPFILES=1

  # python bash completion
  if [ -f ~/.bash_completion.d/python-argcomplete ]; then
      source ~/.bash_completion.d/python-argcomplete
  fi

**NOTE:** This is a work in progress, we are adding more autocomplete
functions.

Currently Supported Data
========================

**USDA Stock database**

- Standard reference database (SR28)  `[7794 foods]`


**Relative USDA Extensions**

- Flavonoid, Isoflavonoids, and Proanthocyanidins  `[1352 foods]`

Usage
=====

Requires internet connection to download initial datasets.
Run ``nutra init`` for this step.

Run the ``nutra`` script to output usage.

Usage: ``nutra [options] <command>``


Commands
########

::

  usage: nutra [-h] [-v] [-d] [--no-pager]
               {init,nt,search,sort,anl,day,recipe} ...

  optional arguments:
    -h, --help            show this help message and exit
    -v, --version         show program's version number and exit
    -d, --debug           enable detailed error messages
    --no-pager            disable paging (print full output)

  nutra subcommands:
    {init,nt,search,sort,anl,day,recipe}
      init                setup profiles, USDA and NT database
      nt                  list out nutrients and their info
      search              search foods by name, list overview info
      sort                sort foods by nutrient ID
      anl                 analyze food(s)
      day                 analyze a DAY.csv file, RDAs optional
      recipe              list and analyze recipes

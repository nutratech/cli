************
 Change Log
************

All notable changes to this project will be documented in this file.

The format is based on `Keep a Change Log <https://keepachangelog.com/en/1.1.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.



[0.2.8] - Unreleased
########################################################################



[0.2.7] - 2023-03-27
########################################################################

Changed
~~~~~~~

- Tweaked dependency versions to work with most older stuff (wip still testing)
- ``n`` vs. ``nutra`` different strategies to work on both Windows/Unix

Fixed
~~~~~

- Added backs scripts to fix ``argcomplete`` in different edge cases
- A couple spots where unsorted dictionaries were causing bugs on older python
- Enhanced some developer experience things (Makefile, GitHub CI/workflows)

Removed
~~~~~~~

- PyPI builds exclude ``tests/`` and unneeded ``requirements-*.txt files``



[0.2.6] - 2022-08-08
########################################################################

Added
~~~~~

- Recipes are stored in a ``csv`` format now with ``uuid`` instead of ``int``,
  and they can be viewed in a convenient ``tree`` output
  (**NOTE:** recipes is still a WIP).
- Calculate functions for body fat, BMR, 1-rep max, & lean body limits.
- Example recipe ``csv`` files.
- ``unittest`` compatibility, not sure this will stay.
  May revert to ``pytest``.
- Dedicated test file for ``calculate.py`` service.

Changed
~~~~~~~

- Use a ``CliConfig`` class for storing ``DEBUG`` and ``PAGING`` flags.
- Requirements versions for ``colorama`` and ``python3.4``.
- Removed ``F401`` warnings, e.g. importing services into ``__init__``.
- General refactor of ``argparse`` stuff, but still not complete.
- Start to split apart some of the original ``test_cli`` functions.
- Enable more verbose ``mypy`` flags.

Fixed
~~~~~

- Faulty algebra in the ``orm_brzycki`` equation.
- Missing rep ranges for ``dos_remedios`` equation.



[0.2.5] - 2022-07-20
########################################################################

Added
~~~~~

- Automated CI/CD integration tests for ``Windows`` platform and multiple
  Python versions.
- Enhanced linting, type checking, and true Python 3.4 compliance.

Changed
~~~~~~~

- Specify version **range** for package dependencies, test old Linux / Python.
- Clean up SQL drivers and Python functions. Use non-plural tables.



[0.2.4] - 2022-07-12
########################################################################

Fixed
~~~~~

- Error when doing a pip install: ``NTSQLITE_DESTINATION`` is not defined.



[0.2.3] - 2022-07-12
########################################################################

Added
~~~~~

- ``[WIP]`` Download cache & checksum verification.
- ``[DEVELOPMENT]`` Added ``Makefile`` with easy commands for ``init``,
  ``lint``, ``test``, etc.
- ``n`` as a shorthand script for ``nutra``.

Changed
~~~~~~~

- Rename to ``CHANGELOG.rst`` (from markdown ``*.md``).

Fixed
~~~~~

- Separate installer logic ``scripts`` & ``entry_points`` for Windows vs. Unix.

Removed
~~~~~~~

- Some tables, e.g. ``biometric``. See ``nt-sqlite`` submodule for details.
  This is still a work in progress to newer tables.



[0.2.2] - 2022-04-08
########################################################################

Added
~~~~~

- Limit search & sort results to top ``n`` results (e.g. top 10 or top 100)
- Enhanced terminal sizing (buffer termination).
- ``Pydoc`` ``PAGING`` flag via ``--no-pager`` command line argument
  (with ``set_flags()`` method).
- Check for appropriate ``ntsqlite`` database version.
- ``[DEVELOPMENT]`` Special ``file_or_dir_path`` and ``file_path``
  custom type validators for ``argparse``.
- ``[DEVELOPMENT]`` Added special requirements files for
  (``test``, ``lint``, ``optional: Levenshtein``,
  and ``win_xp-test`` [Python 3.4]).
- ``[DEVELOPMENT]`` Added ``CHANGELOG.md`` file.

Changed
~~~~~~~

- Print ``exit_code`` in DEBUG mode (`--debug` flag/argument).
- Moved ``subparsers`` module in ``ntclient.argparser`` to ``__init__``.
- Moved tests out of ``ntclient/`` and into ``tests/`` folder.



[0.2.1] - 2021-05-30
########################################################################

Added
~~~~~

- Python 3.4 support (Windows XP and Ubuntu 16.04).
- Debug flag (``--debug | -d``) for all commands.

Changed
~~~~~~~

- Overall structure with main file and ``argparse`` methods.
- Use soft pip requirements ``~=`` instead of ``==``.
- ``DEFAULT`` and ``OVER`` colors.

Removed
~~~~~~~

- ``guid`` columns from ``ntsqlite`` submodule.



[0.2.0] - 2021-05-21
########################################################################

Added
~~~~~

- SQLite support for ``usda`` and ``nt`` schemas
  (removed API calls to remote server).
- Preliminary support for ``recipe`` and ``bio`` sub-commands.
- On-boarding process with ``init`` sub-command.
- Support for ``argcomplete`` on ``bash`` (Linux/macOS).
- Tests in the form of a sole ``test_cli.py`` file.



[0.0.38] - 2020-08-01
########################################################################

Added
~~~~~

- Support for analysis of "day" ``CSV`` files.

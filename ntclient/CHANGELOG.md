# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

-   Download cache & checksum verification
-   Basic functionality of `import` and `export` subcommands
-   `[DEVELOPMENT]` Added `Makefile` with easy commands for `init`, `lint`, `test`, etc

## [0.2.2] - 2022-04-08

### Added

-   Limit search & sort results to top `n` results (e.g. top 10 or top 100)
-   Enhanced terminal sizing (buffer termination)
-   Pydoc PAGING flag via `--no-pager` command line arg (with `set_flags()` method)
-   Check for appropriate `ntsqlite` database version
-   `[DEVELOPMENT]` Special `file_or_dir_path` and `file_path` custom type validators
    for argparse
-   `[DEVELOPMENT]` Added special requirements files for
    (`test`, `lint`, `optional` [Levenshtein], and `win_xp-test` [Python 3.4])
-   `[DEVELOPMENT]` Added `CHANGELOG.md` file

### Changed

-   Print `exit_code` in DEBUG mode (`--debug` flag/arg)
-   Moved `subparsers` module in `ntclient.argparser` to `__init__`
-   Moved tests out of `ntclient/` and into `tests/` folder

## [0.2.1] - 2021-05-30

### Added

-   Python 3.4.3 support (Windows XP and Ubuntu 16.04)
-   Debug flag (`--debug | -d`) for all commands

### Changed

-   Overall structure with main file and argparse methods
-   Use soft pip requirements `~=` instead of `==`
-   `DEFAULT` and `OVER` colors

### Removed

-   guid columns from `ntsqlite` submodule

## [0.2.0] - 2021-05-21

### Added

-   SQLite support for `usda` and `nt` schemas (removed API calls to remote server)
-   Preliminary support for `recipe` and `bio` subcommands
-   On-boarding process with `init` subcommand
-   Support for `argcomplete` on `bash` (Linux/macOS)
-   Tests

## [0.0.38] - 2020-08-01

### Added

-   Support for analysis of day CSV files

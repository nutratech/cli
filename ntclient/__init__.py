# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 16:01:31 2020

@author: shane

This file is part of nutra, a nutrient analysis program.
    https://github.com/nutratech/cli
    https://pypi.org/project/nutra/

nutra is an extensible nutrient analysis and composition application.
Copyright (C) 2018-2022  Shane Jaroch <chown_tee@proton.me>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import os
import platform
import shutil
import sys

from ntclient.ntsqlite.sql import NT_DB_NAME

# Package info
__title__ = "nutra"
__version__ = "0.2.5"
__author__ = "Shane Jaroch"
__email__ = "chown_tee@proton.me"
__license__ = "GPL v3"
__copyright__ = "Copyright 2018-2022 Shane Jaroch"
__url__ = "https://github.com/nutratech/cli"

# Sqlite target versions
__db_target_nt__ = "0.0.6"
__db_target_usda__ = "0.0.8"
USDA_XZ_SHA256 = "25dba8428ced42d646bec704981d3a95dc7943240254e884aad37d59eee9616a"

# Global variables
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
NUTRA_HOME = os.getenv("NUTRA_HOME", os.path.join(os.path.expanduser("~"), ".nutra"))
USDA_DB_NAME = "usda.sqlite"
# NOTE: NT_DB_NAME = "nt.sqlite3" is defined in ntclient.ntsqlite.sql
DEBUG = False
PAGING = True

NTSQLITE_BUILDPATH = os.path.join(ROOT_DIR, "ntsqlite", "sql", NT_DB_NAME)
NTSQLITE_DESTINATION = os.path.join(NUTRA_HOME, NT_DB_NAME)

# Check Python version
PY_MIN_VER = (3, 4, 0)
PY_SYS_VER = sys.version_info[0:3]
PY_MIN_STR = ".".join(str(x) for x in PY_MIN_VER)
PY_SYS_STR = ".".join(str(x) for x in PY_SYS_VER)
if PY_SYS_VER < PY_MIN_VER:
    print("ERROR: %s requires Python %s or later to run" % (__title__, PY_MIN_STR))
    print("HINT:  You're running Python %s" % PY_SYS_STR)
    sys.exit(1)

# Buffer truncation
BUFFER_WD = shutil.get_terminal_size()[0]
BUFFER_HT = shutil.get_terminal_size()[1]

DEFAULT_RESULT_LIMIT = BUFFER_HT - 4

DEFAULT_DAY_H_BUFFER = BUFFER_WD - 4 if BUFFER_WD > 12 else 8

# TODO: keep one extra row on winXP / cmd.exe, it cuts off
DECREMENT = 1 if platform.system() == "Windows" else 0
DEFAULT_SORT_H_BUFFER = (
    BUFFER_WD - (38 + DECREMENT) if BUFFER_WD > 50 else (12 - DECREMENT)
)
DEFAULT_SEARCH_H_BUFFER = (
    BUFFER_WD - (50 + DECREMENT) if BUFFER_WD > 70 else (20 - DECREMENT)
)


# NOTE: wip
# class CLIConfig:
#     def __init__(self):
#         prop1 = True
#         usda_sqlite
#         nt_sqlitedriver


# TODO:
#  Nested nutrient tree, like:
#   http://www.whfoods.com/genpage.php?tname=nutrientprofile&dbid=132
#  Attempt to record errors in failed try/catch block (bottom of __main__.py)
#  Make use of argcomplete.warn(msg) ?


def set_flags(args: argparse.Namespace) -> None:
    """
    Sets
      DEBUG flag
      PAGING flag
        from main (after arg parse). Accessible throughout package
    """
    global DEBUG, PAGING  # pylint: disable=global-statement
    DEBUG = args.debug
    PAGING = not args.no_pager

    if DEBUG:
        print("Console size: %sh x %sw" % (BUFFER_HT, BUFFER_WD))

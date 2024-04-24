# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 16:51:14 2024

@author: shane
"""

# TODO: attach some env props to it, and re-instantiate a CliConfig() class.
#  We're just setting it on the shell, as an env var, before running tests in CI.
#  e.g. the equivalent of putting this early in the __init__ file;
#  os.environ["NUTRA_HOME"] = os.path.join(TEST_HOME, ".nutra.test")
#  ...
#  handle setting up the usda.sqlite3 and nt.sqlite3 files in the test home dir.
#  This will allow us to test the persistence layer, and the API layer, in isolation.

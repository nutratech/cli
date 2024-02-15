# -*- coding: utf-8 -*-
"""
Home to persistence and storage utilities.
Used to have a prefs.json, but was deleted and is planned to be maintained
    in sqlite.

Created on Sat Mar 23 13:09:07 2019

@author: shane
"""
import os

from ntclient import NUTRA_HOME

# TODO: create and maintain prefs.json file?  See if there's a library for that, lol

PREFS_JSON = os.path.join(NUTRA_HOME, "prefs.json")

# if

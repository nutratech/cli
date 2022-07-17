# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 13:09:07 2019

@author: shane
"""

import json
import os

from ntclient import NUTRA_HOME

# TODO: init, handle when it doesn't exist yet
# TODO: prompt to create profile if copying default `prefs.json` with PROFILE_ID: -1
#  (non-existent)
PREFS_FILE = os.path.join(NUTRA_HOME, "prefs.json")
PREFS = {}
PROFILE_ID = None


def persistence_init() -> None:
    """Loads the preferences file and relevant bits"""
    global PREFS, PROFILE_ID  # pylint: disable=global-statement
    from ntclient import DEBUG  # pylint: disable=import-outside-toplevel

    if os.path.isfile(PREFS_FILE):
        with open(PREFS_FILE, encoding="utf-8") as file_path:
            PREFS = json.load(file_path)
    else:
        if DEBUG:
            print("WARN: ~/.nutra/prefs.json doesn't exist, using defaults")
        PREFS = {}

    PROFILE_ID = PREFS.get("current_user")
    if DEBUG and not PROFILE_ID:
        print(
            "WARN: ~/.nutra/prefs.json doesn't contain valid PROFILE_ID,"
            "proceeding in bare mode"
        )

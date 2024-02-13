#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 09:51:48 2024

@author: shane
"""
import os
import traceback

import ntclient.services.api.funcs
from ntclient.persistence.sql.nt import sql as sql_nt


def insert(args: list, exception: Exception) -> None:
    """Insert bug report into nt.sqlite3, return True/False."""
    print("inserting bug reports...", end="")
    sql_nt(
        """
INSERT INTO bug
  (profile_id, arguments, repr, stack, client_info, app_info, user_details)
  VALUES
    (?,?,?,?,?,?,?)
        """,
        (
            1,
            " ".join(args),
            repr(exception),
            os.linesep.join(traceback.format_tb(exception.__traceback__)),
            "client_info",
            "app_info",
            "user_details",
        ),
    )


def submit() -> int:
    """Submit bug reports to developer, return n_submitted."""
    n_submitted = 0
    sql_bugs = sql_nt("SELECT * FROM bug WHERE submitted = 0")
    print(f"submitting {len(sql_bugs)} bug reports...")
    for bug in sql_bugs:
        # print(", ".join(str(x) for x in bug))
        ntclient.services.api.funcs.post_bug(bug)
        n_submitted += 1
    # 1 / 0  # force exception
    # raise Exception("submitting bug reports failed")

    return n_submitted

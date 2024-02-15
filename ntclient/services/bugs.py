#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 09:51:48 2024

@author: shane
"""
import os
import sqlite3
import traceback

import ntclient.services.api
from ntclient.persistence.sql.nt import sql as sql_nt


def insert(args: list, exception: Exception) -> None:
    """Insert bug report into nt.sqlite3, return True/False."""
    print("INFO: inserting bug report...")
    try:
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
    except sqlite3.IntegrityError as exc:
        print(f"WARN: {repr(exc)}")
        if repr(exc) == (
            "IntegrityError('UNIQUE constraint failed: " "bug.arguments, bug.stack')"
        ):
            print("INFO: bug report already exists")
        else:
            raise


def list_bugs() -> list:
    """List all bugs."""
    sql_bugs = sql_nt("SELECT * FROM bug")
    return sql_bugs


def submit_bugs() -> int:
    """Submit bug reports to developer, return n_submitted."""

    # Gather bugs for submission
    sql_bugs = sql_nt("SELECT * FROM bug WHERE submitted = 0")
    api_client = ntclient.services.api.ApiClient()

    n_submitted = 0
    print(f"submitting {len(sql_bugs)} bug reports...")
    print("_" * len(sql_bugs))

    for bug in sql_bugs:
        _res = api_client.post_bug(bug)

        # Differentially store unique vs. duplicate bugs (someone else submitted)
        if _res.status_code == 201:
            sql_nt("UPDATE bug SET submitted = 1 WHERE id = %s", bug.id)
        elif _res.status_code in {200, 204}:
            sql_nt("UPDATE bug SET submitted = 2 WHERE id = %s", bug.id)

        print(".", end="", flush=True)
        n_submitted += 1

    print()

    return n_submitted

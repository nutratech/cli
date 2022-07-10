"""Nutratracker DB specific sqlite module"""
import os
import sqlite3

from ntclient import NT_DB_NAME, NUTRA_DIR, __db_target_nt__
from ntclient.persistence.sql import _sql, version
from ntclient.utils.exceptions import SqlConnectError, SqlInvalidVersionError


def nt_sqlite_connect(version_check=True):
    """Connects to the nt.sqlite3 file, or throws an exception"""
    db_path = os.path.join(NUTRA_DIR, NT_DB_NAME)
    if os.path.isfile(db_path):
        con = sqlite3.connect(db_path)
        con.row_factory = sqlite3.Row

        # Verify version
        if version_check and nt_ver() != __db_target_nt__:
            raise SqlInvalidVersionError(
                "ERROR: nt target [{0}] mismatch actual [{1}] ".format(
                    __db_target_nt__, nt_ver()
                )
                + "upgrades not supported, please remove '~/.nutra/nt.sqlite3'"
                "and re-run 'nutra init'"
            )
        return con

    # Else it's not on disk
    raise SqlConnectError("ERROR: nt database doesn't exist, please run `nutra init`")


def nt_ver():
    """Gets version string for nt.sqlite3 database"""
    con = nt_sqlite_connect(version_check=False)
    return version(con)


def sql(query, values=None, headers=False):
    """Executes a SQL command to nt.sqlite3"""
    con = nt_sqlite_connect()
    return _sql(con, query, db_name="nt", values=values, headers=headers)

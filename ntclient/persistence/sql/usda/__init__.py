"""USDA DB specific sqlite module"""
import os
import sqlite3
import tarfile
import urllib.request
from typing import Union

from ntclient import NUTRA_DIR, USDA_DB_NAME, __db_target_usda__
from ntclient.persistence.sql import _sql, _sql_headers, version
from ntclient.utils.exceptions import SqlConnectError, SqlInvalidVersionError


def usda_init(yes=False) -> None:
    """On-boarding function. Downloads tarball and unpacks usda.sqlite3 file"""

    def input_agree() -> str:
        return input("\nAgree to USDA download, may take minutes? [Y/n] ")

    def download_extract_usda() -> None:
        """Download USDA tarball from BitBucket and extract to storage folder"""

        if yes or input_agree().lower() == "y":
            # TODO: save with version in filename? Don't re-download tarball, just extract?
            save_path = os.path.join(NUTRA_DIR, "%s.tar.xz" % USDA_DB_NAME)

            # Download usda.sqlite3.tar.xz
            print("curl -L %s -o %s.tar.xz" % (url, USDA_DB_NAME))
            urllib.request.urlretrieve(url, save_path)  # nosec: B310

            # Extract the archive
            with tarfile.open(save_path, mode="r:xz") as usda_sqlite_file:
                print("\ntar xvf %s.tar.xz" % USDA_DB_NAME)
                usda_sqlite_file.extractall(NUTRA_DIR)

            print("==> done downloading %s" % USDA_DB_NAME)

    # TODO: handle resource moved on Bitbucket or version mismatch due to manual overwrite?
    url = (
        "https://bitbucket.org/dasheenster/nutra-utils/downloads/{0}-{1}.tar.xz".format(
            USDA_DB_NAME, __db_target_usda__
        )
    )

    if USDA_DB_NAME not in os.listdir(NUTRA_DIR):
        print("INFO: usda.sqlite3 doesn't exist, is this a fresh install?")
        download_extract_usda()
    elif usda_ver() != __db_target_usda__:
        print(
            "INFO: usda.sqlite3 target [{0}] doesn't match actual [{1}], ".format(
                __db_target_usda__, usda_ver()
            )
            + "static resource (no user data lost).. downloading and extracting correct version"
        )
        download_extract_usda()

    if usda_ver() != __db_target_usda__:
        raise SqlInvalidVersionError(
            "ERROR: usda target [{0}] failed to match actual [{1}], ".format(
                __db_target_usda__, usda_ver()
            )
            + "please contact support or try again"
        )


def usda_sqlite_connect(version_check=True) -> sqlite3.Connection:
    """Connects to the usda.sqlite3 file, or throws an exception"""

    # TODO: support as customizable env var ?
    db_path = os.path.join(NUTRA_DIR, USDA_DB_NAME)
    if os.path.isfile(db_path):
        con = sqlite3.connect(db_path)
        # con.row_factory = sqlite3.Row  # see: https://chrisostrouchov.com/post/python_sqlite/

        # Verify version
        if version_check and usda_ver() != __db_target_usda__:
            raise SqlInvalidVersionError(
                "ERROR: usda target [{0}] mismatch actual [{1}], ".format(
                    __db_target_usda__, usda_ver()
                )
                + "remove '~/.nutra/usda.sqlite3' and run 'nutra init'"
            )
        return con

    # Else it's not on disk
    raise SqlConnectError("ERROR: usda database doesn't exist, please run `nutra init`")


def usda_ver() -> str:
    """Gets version string for usda.sqlite3 database"""

    con = usda_sqlite_connect(version_check=False)
    return version(con)


def sql(query, values=None, version_check=True) -> list:
    """Executes a SQL command to usda.sqlite3"""

    con = usda_sqlite_connect(version_check=version_check)

    # TODO: support argument: _sql(..., params=params, ...)
    return _sql(con, query, db_name="usda", values=values)


def sql_headers(query, values=None, version_check=True) -> tuple:
    """Executes a SQL command to usda.sqlite3 [WITH HEADERS]"""

    con = usda_sqlite_connect(version_check=version_check)

    # TODO: support argument: _sql(..., params=params, ...)
    return _sql_headers(con, query, db_name="usda", values=values)

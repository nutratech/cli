"""Services module, currently only home to SQL/persistence init method"""
import os

from ntclient import (
    NTSQLITE_BUILDPATH,
    NTSQLITE_DESTINATION,
    NUTRA_DIR,
    __db_target_nt__,
)
from ntclient.ntsqlite.sql import build_ntsqlite
from ntclient.persistence.sql.nt import nt_ver
from ntclient.persistence.sql.usda import usda_init
from ntclient.services import analyze, recipe, usda
from ntclient.utils.exceptions import SqlInvalidVersionError


def init(yes=False):
    """
    TODO:   Check for:
        1. .nutra folder
        2. usda
        3a. nt
        3b. default profile?
        4. prefs.json
    """
    print("Nutra directory  ", end="")
    if not os.path.isdir(NUTRA_DIR):
        os.makedirs(NUTRA_DIR, 0o755)
    print("..DONE!")

    # TODO: print off checks, return False if failed
    print("USDA db          ", end="")
    usda_init(yes=yes)
    print("..DONE!")

    print("Nutra db         ", end="")
    build_ntsqlite()
    # TODO: don't overwrite,
    #  verbose toggle for download,
    #  option to upgrade
    if os.path.isfile(NTSQLITE_DESTINATION):
        if nt_ver() != __db_target_nt__:
            # TODO: hard requirement? raise error?
            print(
                "WARN: upgrades/downgrades not supported "
                + "(actual: {0} vs. target: {1}), ".format(nt_ver(), __db_target_nt__)
                + "please remove `~/.nutra/nt.sqlite3` file or ignore this warning"
            )
        print("..DONE!")
        os.remove(NTSQLITE_BUILDPATH)  # clean up
    else:
        # TODO: is this logic (and these error messages) the best?
        #  what if .isdir() == True ? Fails with stacktrace?
        os.rename(NTSQLITE_BUILDPATH, NTSQLITE_DESTINATION)
        if not nt_ver() == __db_target_nt__:
            raise SqlInvalidVersionError(
                "ERROR: nt target [{0}] mismatch actual [{1}], ".format(
                    __db_target_nt__, nt_ver()
                )
                + ", please contact support or try again"
            )
        print("..DONE!")

    print("\nAll checks have passed!")
    return 0, True

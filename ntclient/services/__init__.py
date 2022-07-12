"""Services module, currently only home to SQL/persistence init method"""
import os

from ntclient import NUTRA_DIR
from ntclient.ntsqlite.sql import build_ntsqlite
from ntclient.persistence.sql.nt import nt_init
from ntclient.persistence.sql.usda import usda_init
from ntclient.services import analyze, recipe, usda


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
    nt_init()

    print("\nAll checks have passed!")
    return 0, True

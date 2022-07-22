# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 15:33:57 2022

@author: shane
CSV utilities for reading and processing recipes.

TODO: copy to & cache in sqlite3, only look to CSV if it doesn't exist?
 Well then what if they edit CSV... gah.
"""
import glob

from ntclient.services.recipe import RECIPE_HOME


def csv_files() -> list:
    """Returns full filenames for everything under 'f{}/recipe'"""

    return glob.glob(RECIPE_HOME + "/**/*.csv")


def csv_tree() -> tuple:
    """Print off the recipe tree"""
    return 1, 0


def csv_analyze_recipe(uuid: str) -> tuple:
    """Return overview & analysis of a selected recipe"""
    return 1, (str(), "testName")

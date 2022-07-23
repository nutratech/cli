# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 17:12:28 2022

@author: shane

Supporting methods for main service
"""
import os
import shutil

from ntclient import ROOT_DIR
from ntclient.models import Recipe
from ntclient.services.recipe import RECIPE_HOME, csv_utils


def recipes_init(_force: bool = True) -> tuple:
    """
    A filesystem function which copies the stock data into
        os.path.join(NUTRA_HOME, "recipes")
    TODO: put filesystem functions into separate module and ignore in coverage report.

    @return: exit_code: int
    """
    recipes_source = os.path.join(ROOT_DIR, "resources", "recipe")
    recipes_destination = os.path.join(RECIPE_HOME, "core")

    if _force and os.path.exists(recipes_destination):
        print("WARN: force removing core recipes: %s" % recipes_destination)
        # NOTE: is this best?
        shutil.rmtree(recipes_destination, ignore_errors=True)

    try:
        shutil.copytree(recipes_source, recipes_destination)
        return 0, None
    except FileExistsError:
        print("ERROR: file/directory exists: %s")
        print(" remove it, or use the '-f' flag")
        return 1, None


def recipes_overview() -> tuple:
    """
    Shows overview for all recipes.
    TODO: Accept recipes input Tuple[tuple], else read from disk.
    TODO: option to print tree vs. detail view

    @return: exit_code, None
    """

    try:
        csv_utils.csv_recipe_print_tree()
        return 0, None
    except FileNotFoundError:
        print("WARN: no recipes found, create some or run: nutra recipe init")
        return 1, None


def recipe_overview(recipe_path: str) -> tuple:
    """Shows single recipe overview"""
    _recipes = tuple(csv_utils.csv_files())
    recipes = [Recipe(_file_path) for _file_path in _recipes]
    return 0, _recipes

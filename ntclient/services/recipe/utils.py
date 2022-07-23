# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 17:12:28 2022

@author: shane

Supporting methods for main service
"""
import os
import shutil

from ntclient.models import Recipe
from ntclient.services.recipe import RECIPE_HOME, RECIPE_STOCK, csv_utils


def recipes_init(_force: bool = True) -> tuple:
    """
    A filesystem function which copies the stock data into
        os.path.join(NUTRA_HOME, "recipes")
    TODO: put filesystem functions into separate module and ignore in coverage report.

    @return: exit_code: int
    """
    recipes_destination = os.path.join(RECIPE_HOME, "core")

    if _force and os.path.exists(recipes_destination):
        print("WARN: force removing core recipes: %s" % recipes_destination)
        # NOTE: is this best?
        shutil.rmtree(recipes_destination, ignore_errors=True)

    try:
        shutil.copytree(RECIPE_STOCK, recipes_destination)
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

    try:
        _recipe = Recipe(recipe_path)
        _recipe.process_data()
        # TODO: extract relavant bits off, process, use nutprogbar (e.g. day analysis)
        return 0, _recipe
    except (FileNotFoundError, IndexError) as err:
        print("ERROR: %s" % repr(err))
        return 1, None

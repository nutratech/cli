# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 17:12:28 2022

@author: shane

Supporting methods for main service
"""
import glob
import os
import shutil

from tabulate import tabulate

from ntclient import NUTRA_HOME, ROOT_DIR
from ntclient.core.nutprogbar import nutprogbar
from ntclient.persistence.sql.usda.funcs import (
    sql_analyze_foods,
    sql_food_details,
    sql_nutrients_overview,
)
from ntclient.services.recipe import RECIPE_HOME
from ntclient.services.recipe.csv_utils import csv_analyze_recipe, csv_tree


def recipes_init(_copy: bool = True) -> tuple:
    """
    A filesystem function which copies the stock data into f"{NUTRA_HOME}/recipes".
    TODO: put filesystem functions into separate module and ignore in coverage report.

    @return: exit_code: int, copy_count: int
    """
    recipes_source = os.path.join(ROOT_DIR, "resources", "")
    # Create directory if it doesn't exist
    os.makedirs(RECIPE_HOME, 0o775, True)

    csv_files = glob.glob(recipes_source + "/**/*.csv")

    if not _copy:
        return 1, len(csv_files)

    for csv_file in csv_files:
        shutil.copy(csv_file, RECIPE_HOME)
    return 0, len(csv_files)


def recipes_overview(_recipes: tuple = ()) -> tuple:
    """
    Shows overview for all recipes.
    Accepts recipes input Tuple[tuple], else reads from disk to look for some.

    @param _recipes: List[dict] {id, name, tagname, n_foods: int, weight: float}
    @return: exit_code, results: dict
    """

    if not _recipes:
        _, _recipes = csv_tree()
    if not _recipes:
        print(
            "WARN: no recipes. Add to '%s/recipes', or run: n recipe init" % NUTRA_HOME
        )
        return 1, []

    headers = ("id", "name", "tagname", "n_foods", "weight")
    results = []
    for recipe in _recipes:
        result = (
            recipe[0],
            recipe[1],
            recipe[2],
            recipe[3],
            recipe[4],
        )
        results.append(result)

    table = tabulate(results, headers=headers, tablefmt="presto")
    print(table)
    return 0, results


def recipe_overview(recipe_uuid: str, _recipes: tuple = ()) -> tuple:
    """Shows single recipe overview"""
    _, recipe = csv_analyze_recipe(recipe_uuid)
    name = recipe
    print(name)

    food_ids_dict = {x[2]: x[3] for x in recipe}
    food_ids = set(food_ids_dict.keys())
    food_names = {x[0]: x[3] for x in sql_food_details(food_ids)}
    food_analyses = sql_analyze_foods(food_ids)

    table = tabulate(
        [[food_names[food_id], grams] for food_id, grams in food_ids_dict.items()],
        headers=["food", "g"],
    )
    print(table)
    # tabulate nutrient RDA %s
    nutrients = sql_nutrients_overview()
    # rdas = {x[0]: x[1] for x in nutrients.values()}
    progbars = nutprogbar(food_ids_dict, food_analyses, nutrients)
    print(progbars)

    return 0, recipe

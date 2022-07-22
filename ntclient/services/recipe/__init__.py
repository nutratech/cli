# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 15:14:00 2020

@author: shane
Supporting methods for main service
"""
import csv
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
from ntclient.services.recipe.csv_utils import csv_tree


def recipes_init(_copy: bool = True) -> tuple:
    """
    A filesystem function which copies the stock data into f"{NUTRA_HOME}/recipes".
    TODO: put filesystem functions into separate module and ignore in coverage report.

    @return: exit_code: int, copy_count: int
    """
    recipes_source = os.path.join(ROOT_DIR, "resources", "")
    recipes_destination = os.path.join(NUTRA_HOME, "")
    os.makedirs(recipes_destination, 0o775, True)

    csv_files = glob.glob(recipes_source + "/*.csv")

    if not _copy:
        return 1, len(csv_files)

    for csv_file in csv_files:
        shutil.copy(csv_file, recipes_destination)
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

    results = []
    for recipe in _recipes:
        result = {
            "id": recipe[0],
            "name": recipe[2],
            "tagname": recipe[1],
            "n_foods": recipe[3],
            "weight": recipe[4],
        }
        results.append(result)

    table = tabulate(results, headers="keys", tablefmt="presto")
    print(table)
    return 0, results


def recipe_overview(recipe_id: int, _recipes: tuple = ()) -> tuple:
    """Shows single recipe overview"""
    recipe = sql_analyze_recipe(recipe_id)
    name = recipe[0][1]
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

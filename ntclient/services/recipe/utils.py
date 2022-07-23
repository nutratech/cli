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
from ntclient.services.recipe.csv_utils import (
    csv_analyze_recipe,
    csv_files,
    csv_print_tree,
)


def recipes_init(_force: bool = True) -> tuple:
    """
    A filesystem function which copies the stock data into
        os.path.join(NUTRA_HOME, "recipes")
    TODO: put filesystem functions into separate module and ignore in coverage report.

    @return: exit_code: int
    """
    recipes_source = os.path.join(ROOT_DIR, "resources", "recipe")
    recipes_destination = os.path.join(RECIPE_HOME, "core")

    if _force:
        print("WARN: force removing core recipes: %s" % recipes_destination)
        shutil.rmtree(recipes_destination)

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

    @param _recipes: List[dict] {id, name, tagname, n_foods: int, weight: float}
    @return: exit_code, results: dict
    """

    csv_print_tree()
    return 0, None


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

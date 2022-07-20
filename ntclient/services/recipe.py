#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 15:14:00 2020

@author: shane
"""
import csv
import os

from tabulate import tabulate

from ntclient.core.nutprogbar import nutprogbar
from ntclient.persistence.sql.nt.funcs import (
    sql_analyze_recipe,
    sql_nt_next_index,
    sql_recipe,
    sql_recipes,
)
from ntclient.persistence.sql.usda.funcs import (
    sql_analyze_foods,
    sql_food_details,
    sql_nutrients_overview,
)


def recipes_overview() -> tuple:
    """Shows overview for all recipes"""
    recipes = sql_recipes()[1]

    results = []
    for recipe in recipes:
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


def recipe_overview(recipe_id: int) -> tuple:
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


def recipe_import(file_path: str) -> tuple:
    """Import a recipe to SQL database"""

    def extract_id_from_filename(path: str) -> int:
        filename = str(os.path.basename(path))
        if (
            "[" in filename
            and "]" in filename
            and filename.index("[") < filename.index("]")
        ):
            # TODO: try, raise: print/warn
            return int(filename.split("[")[1].split("]")[0])
        return 0  # zero is falsy

    if os.path.isfile(file_path):
        # TODO: better logic than this
        recipe_id = extract_id_from_filename(file_path) or sql_nt_next_index("recipe")
        print(recipe_id)
        with open(file_path, encoding="utf-8") as file:
            reader = csv.DictReader(file)
            # headers = next(reader)
            rows = list(reader)
        print(rows)
    else:  # os.path.isdir()
        print("not implemented ;]")
    return 1, False


def recipe_add(name: str, food_amts: dict) -> tuple:
    """Add a recipe to SQL database"""
    print()
    print("New recipe: " + name + "\n")

    food_ids = set(food_amts.keys())
    food_names = {x[0]: x[2] for x in sql_food_details(food_ids)}

    results = []
    for food_id, grams in food_amts.items():
        results.append([food_id, food_names[food_id], grams])

    table = tabulate(results, headers=["id", "food_name", "grams"], tablefmt="presto")
    print(table)

    confirm = input("\nCreate recipe? [Y/n] ")

    if confirm.lower() == "y":
        print("not implemented ;]")
    return 1, False


def recipe_delete(recipe_id: int) -> tuple:
    """Deletes recipe by ID, along with any FK constraints"""
    recipe = sql_recipe(recipe_id)[0]

    print(recipe[4])
    confirm = input("Do you wish to delete? [Y/n] ")

    if confirm.lower() == "y":
        print("not implemented ;]")
    return 1, False

# -*- coding: utf-8 -*-
"""
Current home to subparsers and service-level logic.
These functions all return a tuple of (exit_code: int, results: list|dict).

Created on Sat Jul 18 16:30:28 2020 -0400

@author: shane
"""
import argparse
import os
from datetime import datetime

import ntclient.services.analyze
import ntclient.services.recipe.utils
import ntclient.services.usda
from ntclient import Gender, activity_factor_from_index
from ntclient.services import calculate as calc


def init(args: argparse.Namespace) -> tuple:
    """Wrapper init method for persistence stuff"""
    return ntclient.services.init(yes=args.yes)


##############################################################################
# Nutrients, search and sort
##############################################################################
def nutrients() -> tuple:
    """List nutrients"""
    return ntclient.services.usda.list_nutrients()


def search(args: argparse.Namespace) -> tuple:
    """Searches all dbs, foods, recipes, recent items and favorites."""
    if args.top:
        return ntclient.services.usda.search(
            words=args.terms, fdgrp_id=args.fdgrp_id, limit=args.top
        )
    return ntclient.services.usda.search(words=args.terms, fdgrp_id=args.fdgrp_id)


def sort(args: argparse.Namespace) -> tuple:
    """Sorts based on nutrient id"""
    if args.top:
        return ntclient.services.usda.sort_foods(
            args.nutr_id, by_kcal=args.kcal, limit=args.top
        )
    return ntclient.services.usda.sort_foods(args.nutr_id, by_kcal=args.kcal)


##############################################################################
# Analysis and Day scoring
##############################################################################
def analyze(args: argparse.Namespace) -> tuple:
    """Analyze a food"""
    # exc: ValueError,
    food_ids = set(args.food_id)
    grams = float(args.grams) if args.grams else 0.0

    return ntclient.services.analyze.foods_analyze(food_ids, grams)


def day(args: argparse.Namespace) -> tuple:
    """Analyze a day's worth of meals"""
    day_csv_paths = [str(os.path.expanduser(x)) for x in args.food_log]
    rda_csv_path = str(os.path.expanduser(args.rda)) if args.rda else str()

    return ntclient.services.analyze.day_analyze(
        day_csv_paths, rda_csv_path=rda_csv_path
    )


##############################################################################
# Recipes
##############################################################################
def recipes_init(args: argparse.Namespace) -> tuple:
    """Copy example/stock data into RECIPE_HOME"""
    _force = args.force

    return ntclient.services.recipe.utils.recipes_init(_force=_force)


def recipes() -> tuple:
    """Show all, in tree or detail view"""
    return ntclient.services.recipe.utils.recipes_overview()


def recipe(args: argparse.Namespace) -> tuple:
    """
    View and analyze a single (or a range)
    @todo: argcomplete based on RECIPE_HOME folder
    @todo: use as default command? Currently this is reached by `nutra recipe anl`
    """
    recipe_path = args.path

    return ntclient.services.recipe.utils.recipe_overview(recipe_path=recipe_path)


##############################################################################
# Calculators
##############################################################################
def calc_1rm(args: argparse.Namespace) -> tuple:
    """Perform 1-rep max calculations"""

    weight = float(args.weight)
    reps = int(args.reps)

    print(reps, weight)
    print("Not implemented yet.")
    print("TODO: transfer service logic from server repository over here.")

    return 0, None


def calc_bmr(args: argparse.Namespace) -> tuple:
    """
    Perform BMR & TDEE calculations

    Example POST:
    {
        "weight": 71,
        "height": 177,
        "gender": "MALE",
        "dob": 725864400,
        "bodyFat": 0.14,
        "activityFactor": 0.55
    }
    """

    weight = float(args.weight)  # kg
    height = float(args.height)  # cm
    gender = Gender(args.gender)
    dob = datetime.fromisoformat(args.dob)  # e.g. 1970-01-01
    body_fat = float(args.body_fat)
    activity_factor = activity_factor_from_index(args.activity_factor)

    print(weight, height, gender, dob, body_fat, activity_factor)
    print("Not implemented yet.")
    print("TODO: transfer service logic from server repository over here.")
    print("TODO: add test in section: nt / arg parser.")

    return 0, None


def calc_body_fat(args: argparse.Namespace) -> tuple:
    """
    Perform body fat calculations for Navy, 3-Site, and 7-Site.

    Example POST. @note FEMALE, also includes "hip" (cm)
    {
        "gender": "MALE",
        "age": 29,
        "height": 178,
        "waist": 80,
        "neck": 36.8,
        // also: hip, if FEMALE
        "chest": 5,
        "abd": 6,
        "thigh": 9,
        "tricep": 6,
        "sub": 8,
        "sup": 7,
        "mid": 4
    }
    """

    gender = Gender.FEMALE if args.female_gender else Gender.MALE
    print("Gender: %s" % gender)

    try:
        _navy = calc.bf_navy(gender, args)
    except (TypeError, ValueError):
        print(
            "WARN: Navy failed, requires: gender, height, waist, neck, "
            "and (if female) hip."
        )
        _navy = 0.0
    try:
        _3site = calc.bf_3site(gender, args)
    except (TypeError, ValueError):
        print(
            "WARN: 3-Site failed, requires: gender, age, chest (mm), "
            "abdominal (mm), and thigh (mm)."
        )
        _3site = 0.0
    try:
        _7site = calc.bf_7site(gender, args)
    except (TypeError, ValueError):
        print(
            "WARN: 7-Site failed, requires: gender, age, chest (mm), "
            "abdominal (mm), thigh (mm), tricep (mm), sub (mm), sup (mm), and mid (mm)."
        )
        _7site = 0.0

    print()
    print("Navy: %s%%" % _navy)
    print("3-Site: %s%%" % _3site)
    print("7-Site: %s%%" % _7site)

    return 0, {"navy": _navy}

# -*- coding: utf-8 -*-
"""
Current home to subparsers and service-level logic.
These functions all return a tuple of (exit_code: int, results: list|dict).

Created on Sat Jul 18 16:30:28 2020 -0400

@author: shane
"""
import argparse
import os
import traceback

from tabulate import tabulate

import ntclient.services.analyze
import ntclient.services.recipe.utils
import ntclient.services.usda
from ntclient import CLI_CONFIG, Gender, activity_factor_from_index
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
    print("Weight: %s" % weight)
    reps = int(args.reps)
    print("Reps:   %s" % reps)

    _epley = calc.orm_epley(weight, reps)
    _brzycki = calc.orm_brzycki(weight, reps)
    _dos_remedios = calc.orm_dos_remedios(weight, reps)

    print("EPLEY")
    _epley_table = tabulate(
        list(_epley.items()), headers=["reps", "epley"], tablefmt="simple"
    )
    print(_epley_table)

    print("BRZYCKI")
    _brzycki_table = tabulate(
        list(_brzycki.items()), headers=["reps", "brzycki"], tablefmt="simple"
    )
    print(_brzycki_table)

    print("DOS REMEDIOS")
    _dos_remedios_table = tabulate(
        list(_dos_remedios.items()), headers=["reps", "dos_remedios"], tablefmt="simple"
    )
    print(_dos_remedios_table)

    return 0, {"epley": _epley, "brzycki": _brzycki, "dos_remedios": _dos_remedios}


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

    activity_factor = activity_factor_from_index(args.activity_factor)

    # TODO: require these all for any? Or do exception handling & optional args like bf?
    _katch_mcardle = calc.bmr_katch_mcardle(activity_factor, args=args)
    _cunningham = calc.bmr_cunningham(activity_factor, args=args)
    _mifflin_st_jeor = calc.bmr_mifflin_st_jeor(activity_factor, args=args)

    result = {
        "katch_mcardle": _katch_mcardle,
        "cunningham": _cunningham,
        "mifflin_st_jeor": _mifflin_st_jeor,
    }

    # Prepare the table for printing
    headers = ("Equation", "BMR", "TDEE")
    rows = []
    for _equation, _calculation in result.items():
        row = [_equation]
        row.extend(_calculation.values())
        rows.append(row)

    _katch_mcardle_table = tabulate(rows, headers=headers, tablefmt="simple")
    print(_katch_mcardle_table)

    return 0, result


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
        print()
        if CLI_CONFIG.debug:
            traceback.print_exc()
        print(
            "WARN: Navy failed, requires: gender, height, waist, neck, "
            "and (if female) hip."
        )
        _navy = 0.0
    try:
        _3site = calc.bf_3site(gender, args)
    except (TypeError, ValueError):
        print()
        if CLI_CONFIG.debug:
            traceback.print_exc()
        print(
            "WARN: 3-Site failed, requires: gender, age, chest (mm), "
            "abdominal (mm), and thigh (mm)."
        )
        _3site = 0.0
    try:
        _7site = calc.bf_7site(gender, args)
    except (TypeError, ValueError):
        print()
        if CLI_CONFIG.debug:
            traceback.print_exc()
        print(
            "WARN: 7-Site failed, requires: gender, age, chest (mm), "
            "abdominal (mm), thigh (mm), tricep (mm), sub (mm), sup (mm), and mid (mm)."
        )
        _7site = 0.0

    _table = tabulate([(_navy, _3site, _7site)], headers=["Navy", "3-Site", "7-Site"])
    print()
    print()
    print(_table)

    return 0, {"navy": _navy, "threeSite": _3site, "sevenSite": _7site}

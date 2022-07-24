# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 16:30:28 2020 -0400

@author: shane
Current home to subparsers and service-level logic
"""
import argparse
import os

from ntclient import services
from ntclient.services.recipe import utils as r_service


def init(args: argparse.Namespace) -> tuple:
    """Wrapper init method for persistence stuff"""
    return services.init(yes=args.yes)


##############################################################################
# Nutrients, search and sort
##############################################################################
def nutrients():  # type: ignore
    """List nutrients"""
    return services.usda.list_nutrients()


def search(args: argparse.Namespace) -> tuple:
    """Searches all dbs, foods, recipes, recent items and favorites."""
    if args.top:
        return services.usda.search(
            words=args.terms, fdgrp_id=args.fdgrp_id, limit=args.top
        )
    return services.usda.search(words=args.terms, fdgrp_id=args.fdgrp_id)


def sort(args: argparse.Namespace) -> tuple:
    """Sorts based on nutrient id"""
    if args.top:
        return services.usda.sort_foods(args.nutr_id, by_kcal=args.kcal, limit=args.top)
    return services.usda.sort_foods(args.nutr_id, by_kcal=args.kcal)


##############################################################################
# Analysis and Day scoring
##############################################################################
def analyze(args: argparse.Namespace) -> tuple:
    """Analyze a food"""
    # exc: ValueError,
    food_ids = set(args.food_id)
    grams = float(args.grams) if args.grams else 0.0

    return services.analyze.foods_analyze(food_ids, grams)


def day(args: argparse.Namespace) -> tuple:
    """Analyze a day's worth of meals"""
    day_csv_paths = [str(os.path.expanduser(x)) for x in args.food_log]
    rda_csv_path = str(os.path.expanduser(args.rda)) if args.rda else str()

    return services.analyze.day_analyze(day_csv_paths, rda_csv_path=rda_csv_path)


##############################################################################
# Recipes
##############################################################################
def recipes_init(args: argparse.Namespace) -> tuple:
    """Copy example/stock data into RECIPE_HOME"""
    _force = args.force

    return r_service.recipes_init(_force=_force)


def recipes() -> tuple:
    """Show all, in tree or detail view"""
    return r_service.recipes_overview()


def recipe(args: argparse.Namespace) -> tuple:
    """View and analyze a single (or a range)"""
    recipe_path = args.path

    return r_service.recipe_overview(recipe_path)

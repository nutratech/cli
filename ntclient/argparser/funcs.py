#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 16:30:28 2020 -0400

@author: shane
Current home to subparsers and service-level logic
"""
import argparse
import os

from ntclient import services


def init(args: argparse.Namespace) -> tuple:
    """Wrapper init method for persistence stuff"""
    return services.init(yes=args.yes)


################################################################################
# Nutrients, search and sort
################################################################################
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


################################################################################
# Analysis and Day scoring
################################################################################
def analyze(args: argparse.Namespace) -> tuple:
    """Analyze a food"""
    food_ids = args.food_id
    grams = args.grams

    return services.analyze.foods_analyze(food_ids, grams)


def day(args: argparse.Namespace) -> tuple:
    """Analyze a day's worth of meals"""
    day_csv_paths = [str(os.path.expanduser(x)) for x in args.food_log]
    rda_csv_path = str(os.path.expanduser(args.rda)) if args.rda else str()

    return services.analyze.day_analyze(day_csv_paths, rda_csv_path=rda_csv_path)


################################################################################
# Recipes
################################################################################
def recipes_init() -> tuple:
    """Copy over stock recipes into 'f{NUTRA_HOME}/recipes'"""
    return services.recipe.recipes_init()


def recipes() -> tuple:
    """Return recipes"""
    return services.recipe.recipes_overview()


def recipe(args: argparse.Namespace) -> tuple:
    """Return recipe view (analysis)"""
    return services.recipe.recipe_overview(args.recipe_id)


def recipe_import(args: argparse.Namespace) -> tuple:
    """Add a recipe"""
    # TODO: custom serving sizes, not always in grams?
    return services.recipe.recipe_import(args.path)


def recipe_delete(args: argparse.Namespace) -> tuple:
    """Delete a recipe"""
    return services.recipe.recipe_delete(args.recipe_id)

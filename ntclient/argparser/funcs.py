"""Current home to subparsers and service-level logic"""
import os

from ntclient import services


def init(args):
    """Wrapper init method for persistence stuff"""
    return services.init(yes=args.yes)


################################################################################
# Nutrients, search and sort
################################################################################
def nutrients():
    """List nutrients"""
    return services.usda.list_nutrients()


def search(args):
    """Searches all dbs, foods, recipes, recents and favorites."""
    if args.top:
        return services.usda.search(
            words=args.terms, fdgrp_id=args.fdgrp_id, limit=args.top
        )
    return services.usda.search(words=args.terms, fdgrp_id=args.fdgrp_id)


def sort(args):
    """Sorts based on nutrient id"""
    if args.top:
        return services.usda.sort_foods(args.nutr_id, by_kcal=args.kcal, limit=args.top)
    return services.usda.sort_foods(args.nutr_id, by_kcal=args.kcal)


################################################################################
# Analysis and Day scoring
################################################################################
def analyze(args):
    """Analyze a food"""
    food_ids = args.food_id
    grams = args.grams

    return services.analyze.foods_analyze(food_ids, grams)


def day(args):
    """Analyze a day's worth of meals"""
    day_csv_paths = args.food_log
    day_csv_paths = [os.path.expanduser(x) for x in day_csv_paths]
    rda_csv_path = os.path.expanduser(args.rda) if args.rda else None

    return services.analyze.day_analyze(day_csv_paths, rda_csv_path=rda_csv_path)


################################################################################
# Biometrics
################################################################################
def bio():
    """List biometrics"""
    return services.biometrics.biometrics()


def bio_log():
    """List biometric logs"""
    return services.biometrics.biometric_logs()


def bio_log_add(args):
    """Add a biometric log entry"""
    bio_vals = {
        int(x.split(",")[0]): float(x.split(",")[1]) for x in args.biometric_val
    }

    return services.biometrics.biometric_add(bio_vals)


################################################################################
# Recipes
################################################################################
def recipes():
    """Return recipes"""
    return services.recipe.recipes_overview()


def recipe(args):
    """Return recipe view (analysis)"""
    return services.recipe.recipe_overview(args.recipe_id)


def recipe_import(args):
    """Add a recipe"""
    # TODO: custom serving sizes, not always in grams?
    return services.recipe.recipe_import(args.path)


def recipe_delete(args):
    """Delete a recipe"""
    return services.recipe.recipe_delete(args.recipe_id)

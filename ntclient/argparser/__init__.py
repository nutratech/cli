"""Main module for things related to argparse"""
import argparse

from ntclient.argparser import funcs as parser_funcs
from ntclient.argparser import types


def build_subcommands(subparsers: argparse._SubParsersAction) -> None:
    """Attaches subcommands to main parser"""
    build_init_subcommand(subparsers)
    build_nt_subcommand(subparsers)
    build_search_subcommand(subparsers)
    build_sort_subcommand(subparsers)
    build_analyze_subcommand(subparsers)
    build_day_subcommand(subparsers)
    build_recipe_subcommand(subparsers)


################################################################################
# Methods to build subparsers, and attach back to main arg_parser
################################################################################
def build_init_subcommand(subparsers: argparse._SubParsersAction) -> None:
    """Self running init command"""
    init_parser = subparsers.add_parser(
        "init", help="setup profiles, USDA and NT database"
    )
    init_parser.add_argument(
        "-y",
        dest="yes",
        action="store_true",
        help="automatically agree to (potentially slow) USDA download",
    )
    init_parser.set_defaults(func=parser_funcs.init)


def build_nt_subcommand(subparsers: argparse._SubParsersAction) -> None:
    """Lists out nutrients details with computed totals and averages"""
    nutrient_parser = subparsers.add_parser(
        "nt", help="list out nutrients and their info"
    )
    nutrient_parser.set_defaults(func=parser_funcs.nutrients)


def build_search_subcommand(subparsers: argparse._SubParsersAction) -> None:
    """Search: terms [terms ... ]"""
    search_parser = subparsers.add_parser(
        "search", help="search foods by name, list overview info"
    )
    search_parser.add_argument(
        "terms",
        nargs="+",
        help='search query, e.g. "grass fed beef" or "ultraviolet mushrooms"',
    )
    search_parser.add_argument(
        "-t",
        dest="top",
        metavar="N",
        type=int,
        help="show top N results (defaults to console height)",
    )
    search_parser.add_argument(
        "-g",
        dest="fdgrp_id",
        type=int,
        help="filter by a specific food group ID",
    )
    search_parser.set_defaults(func=parser_funcs.search)


def build_sort_subcommand(subparsers: argparse._SubParsersAction) -> None:
    """Sort foods ranked by nutr_id, per 100g or 200kcal"""
    sort_parser = subparsers.add_parser("sort", help="sort foods by nutrient ID")
    sort_parser.add_argument(
        "-c",
        dest="kcal",
        action="store_true",
        help="sort by value per 200 kcal, instead of per 100 g",
    )
    sort_parser.add_argument(
        "-t",
        dest="top",
        metavar="N",
        type=int,
        help="show top N results (defaults to console height)",
    )
    sort_parser.add_argument("nutr_id", type=int)
    sort_parser.set_defaults(func=parser_funcs.sort)


def build_analyze_subcommand(subparsers: argparse._SubParsersAction) -> None:
    """Analyzes (foods only for now)"""
    analyze_parser = subparsers.add_parser("anl", help="analyze food(s)")
    analyze_parser.add_argument(
        "-g",
        dest="grams",
        type=float,
        help="scale to custom number of grams (default is 100g)",
    )
    analyze_parser.add_argument("food_id", type=int, nargs="+")
    analyze_parser.set_defaults(func=parser_funcs.analyze)


def build_day_subcommand(subparsers: argparse._SubParsersAction) -> None:
    """Analyzes a DAY.csv, uses new colored progress bar spec"""
    day_parser = subparsers.add_parser(
        "day", help="analyze a DAY.csv file, RDAs optional"
    )
    day_parser.add_argument(
        "food_log",
        metavar="food_log.csv",
        nargs="+",
        type=types.file_or_dir_path,
        help="path to CSV file of food log",
    )
    day_parser.add_argument(
        "-r",
        dest="rda",
        metavar="rda.csv",
        type=types.file_path,
        help="provide a custom RDA file in csv format",
    )
    day_parser.set_defaults(func=parser_funcs.day)


def build_recipe_subcommand(subparsers: argparse._SubParsersAction) -> None:
    """View, add, edit, delete recipes"""
    recipe_parser = subparsers.add_parser("recipe", help="list and analyze recipes")
    recipe_subparsers = recipe_parser.add_subparsers(title="recipe subcommands")

    recipe_anl_parser = recipe_subparsers.add_parser(
        "anl", help="view and analyze for recipe"
    )
    recipe_anl_parser.add_argument(
        "recipe_id", type=int, help="view (and analyze) recipe by ID"
    )
    recipe_anl_parser.set_defaults(func=parser_funcs.recipe)

    recipe_import_parser = recipe_subparsers.add_parser("import", help="add a recipe")
    recipe_import_parser.add_argument(
        "path",
        type=types.file_or_dir_path,
        help="path to recipe.csv (or folder with multiple CSV files)",
    )
    recipe_import_parser.set_defaults(func=parser_funcs.recipe_import)

    # TODO: edit.. support renaming, and overwriting/re-importing food_amts (from CSV)

    recipe_delete_parser = recipe_subparsers.add_parser(
        "delete", help="delete a recipe(s) by ID or range"
    )
    recipe_delete_parser.add_argument("recipe_id", type=int, help="delete recipe by ID")
    recipe_delete_parser.set_defaults(func=parser_funcs.recipe_delete)

    recipe_parser.set_defaults(func=parser_funcs.recipes)

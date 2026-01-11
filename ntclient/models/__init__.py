# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 15:34:07 2022

@author: shane
Classes, structures for storing, displaying, and editing data.
"""
import csv

from ntclient.utils import CLI_CONFIG


class Recipe:
    """Allows reading up CSV, filtering by UUID, and displaying detail view"""

    def __init__(self, file_path: str) -> None:
        """Initialize entity"""

        self.file_path = file_path
        self.csv_reader = csv.DictReader(str())

        # Defined now, populated later
        self.headers = tuple()  # type: ignore
        self.rows = tuple()  # type: ignore

        self.uuid = str()

        self.food_data = {}  # type: ignore

    def _aggregate_rows(self) -> tuple:
        """Aggregate rows into a tuple"""
        print("Processing recipe file: %s" % self.file_path)
        with open(self.file_path, "r", encoding="utf-8") as _file:
            self.csv_reader = csv.DictReader(_file)
            return tuple(list(self.csv_reader))

    def process_data(self) -> None:
        """
        Parses out the raw CSV input read in during self.__init__()
        TODO: test this with an empty CSV file, one with missing or corrupt values
              (e.g. empty or non-numeric grams or food_id).
        TODO: test with a CSV file that has duplicate recipe_id/uuid values.
        TODO: how is the recipe home directory determined here?
        """

        # Read into memory
        self.rows = self._aggregate_rows()

        # Validate data
        uuids = {x["recipe_id"] for x in self.rows}
        if len(uuids) != 1:
            print("ERROR: Found %s keys: %s" % (len(uuids), uuids))
            raise KeyError("FATAL: must have exactly 1 uuid per recipe CSV file!")
        self.uuid = list(uuids)[0]

        # exc: ValueError (could not cast int / float)
        self.food_data = {int(x["food_id"]): float(x["grams"]) for x in self.rows}

        if CLI_CONFIG.debug:
            print("Finished with recipe.")

    def print_analysis(self, scale: float = 0, scale_mode: str = "kcal") -> None:
        """Run analysis on a single recipe"""
        from ntclient import BUFFER_WD
        from ntclient.persistence.sql.usda.funcs import (
            sql_analyze_foods,
            sql_nutrients_overview,
        )
        from ntclient.services.analyze import day_format

        # Get nutrient overview (RDAs, units, etc.)
        nutrients_rows = sql_nutrients_overview()
        nutrients = {int(x[0]): tuple(x) for x in nutrients_rows.values()}

        # Analyze foods in the recipe
        food_ids = set(self.food_data.keys())
        foods_analysis = {}
        for food in sql_analyze_foods(food_ids):
            food_id = int(food[0])
            # nut_id, val (per 100g)
            anl = (int(food[1]), float(food[2]))
            if food_id not in foods_analysis:
                foods_analysis[food_id] = [anl]
            else:
                foods_analysis[food_id].append(anl)

        # Compute totals
        nutrient_totals = {}
        total_weight = 0.0
        for food_id, grams in self.food_data.items():
            total_weight += grams
            if food_id not in foods_analysis:
                continue
            for _nutrient in foods_analysis[food_id]:
                nutr_id = _nutrient[0]
                nutr_per_100g = _nutrient[1]
                nutr_val = grams / 100 * nutr_per_100g
                if nutr_id not in nutrient_totals:
                    nutrient_totals[nutr_id] = nutr_val
                else:
                    nutrient_totals[nutr_id] += nutr_val

        # Print results using day_format for consistency
        buffer = BUFFER_WD - 4 if BUFFER_WD > 4 else BUFFER_WD
        day_format(
            nutrient_totals,
            nutrients,
            buffer=buffer,
            scale=scale,
            scale_mode=scale_mode,
            total_weight=total_weight,
        )

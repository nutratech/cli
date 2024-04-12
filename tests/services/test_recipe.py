# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 21:36:43 2022

@author: shane
"""
import os
import unittest
from unittest.mock import patch

import pytest

import ntclient.services.recipe.utils as r
from ntclient.services.recipe import RECIPE_STOCK, csv_utils


class TestRecipe(unittest.TestCase):
    """Tests the recipe service"""

    def test_recipes_init(self):
        """Checks the init function, which copies over default data (if not already)"""

        exit_code, _result = r.recipes_init(_force=False)
        assert exit_code in {0, 1}

        exit_code, _result = r.recipes_init(_force=True)
        assert exit_code in {0, 1}

    def test_recipes_overview(self):
        """Test type coercion and one-to-one input/output relationship"""

        exit_code, _ = r.recipes_overview()
        assert exit_code == 0

    @unittest.skip("Not implemented")
    def test_recipes_overview_process_data_dupe_recipe_uuids_throws_key_error(self):
        """Raises key error if recipe uuids are not unique"""
        # TODO: return_value should be a list of recipe dicts, each with a 'uuid' key
        with patch("ntclient.models.Recipe.rows", return_value={1, 2}):
            with pytest.raises(KeyError):
                r.recipes_overview()

    def test_recipe_overview_returns_exit_code_1_for_nonexistent_path(self):
        """Returns (1, None) if recipe path is invalid"""

        # TODO: should we be using guid / uuid instead of integer id?
        result = r.recipe_overview("-12345-FAKE-PATH-")
        assert (1, None) == result

    def test_recipe_overview_might_succeed_for_maybe_existing_id(self):
        """Tries 'check for existing ID', but only can if the user initialized"""
        exit_code, _ = r.recipe_overview(
            os.path.join(RECIPE_STOCK, "dinner", "burrito-bowl.csv")
        )
        assert exit_code in {0, 1}

    def test_recipe_csv_utils(self):
        """Test the (largely unused) CSV utils module"""
        _csv_files = csv_utils.csv_files()
        assert _csv_files

        _csv_recipes = csv_utils.csv_recipes()
        assert _csv_recipes

        # sanity executions
        csv_utils.csv_recipe_print_tree()
        csv_utils.csv_print_details()

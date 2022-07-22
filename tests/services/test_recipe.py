# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 21:36:43 2022

@author: shane
"""
import unittest

import pytest

import ntclient.services.recipe.utils as r


class TestRecipe(unittest.TestCase):
    """Tests the recipe service"""

    def test_recipes_init(self):
        """Checks the init function, which copies over default data (if not already)"""
        exit_code, copy_count = r.recipes_init(_copy=False)
        assert exit_code == 1
        assert copy_count == 3

        exit_code, copy_count = r.recipes_init()
        assert exit_code == 0
        assert copy_count == 3

    def test_recipes_overview(self):
        """Test type coercion and one-to-one input/output relationship"""
        exit_code, _recipes = r.recipes_overview()

        assert exit_code == 1
        assert isinstance(_recipes, list)

        exit_code, _recipes_overview = r.recipes_overview(
            _recipes=(
                (1, "test1", "tag1", 10, 75),
                (2, "test2", "tag2", 15, 100),
                (999, "test999", "tag999", 2, 5),
            )
        )

        assert exit_code == 0
        assert len(_recipes_overview) == 3

    def test_recipe_overview_throws_exc_for_negative_id(self):
        """Raises index error if recipe int id is invalid"""
        # TODO: should we be using guid / uuid instead of integer id?
        with pytest.raises(IndexError):
            r.recipe_overview(-12345)

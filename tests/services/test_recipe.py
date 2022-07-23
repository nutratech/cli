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

        exit_code, _result = r.recipes_init(_force=False)
        assert exit_code in {0, 1}

        exit_code, _result = r.recipes_init(_force=True)
        assert exit_code in {0, 1}

    def test_recipes_overview(self):
        """Test type coercion and one-to-one input/output relationship"""

        exit_code, _ = r.recipes_overview()
        assert exit_code == 0

    def test_recipe_overview_throws_exc_for_negative_id(self):
        """Raises index error if recipe int id is invalid"""

        # TODO: should we be using guid / uuid instead of integer id?
        with pytest.raises(IndexError):
            r.recipe_overview(-12345)

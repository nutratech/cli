#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 21:36:43 2022

@author: shane
"""
import pytest

import ntclient.services.recipe as r


def test_recipes_overview():
    exit_code, _recipes = r.recipes_overview()

    assert exit_code == 0
    assert isinstance(_recipes, list)

    exit_code, _recipes = r.recipes_overview(
        (
            (1, "test1", "tag1", 10, 75),
            (2, "test2", "tag2", 15, 100),
            (999, "test999", "tag999", 2, 5),
        )
    )

    assert exit_code == 0
    assert len(_recipes) == 3


def test_recipe_overview_throws_exc_for_negative_id():
    # TODO: should we be using guid / uuid instead of integer id?
    with pytest.raises(IndexError):
        r.recipe_overview(-12345)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 16:14:03 2024

@author: shane
"""
from unittest.mock import MagicMock, patch

from ntclient.services.api import cache_mirrors


@patch("requests.get",return_value=MagicMock(status_code=200))
# pylint: disable=unused-argument
def test_cache_mirrors(*args: MagicMock) -> None:
    """Test cache_mirrors"""
    assert cache_mirrors() == "https://api.dev.nutra.tk"


@patch("requests.get",return_value=MagicMock(status_code=503))
# pylint: disable=unused-argument
def test_cache_mirrors_empty_string_on_failed_mirrors(*args: MagicMock) -> None:
    """Test cache_mirrors"""
    assert cache_mirrors() == str()

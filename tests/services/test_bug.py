# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 16:18:08 2024

@author: shane
"""
import unittest
from unittest.mock import MagicMock, patch

import pytest

from ntclient.__main__ import main
from ntclient.services import bugs


class TestBug(unittest.TestCase):
    """Tests the bug service"""

    def test_bug_simulate(self) -> None:
        """Tests the functions for simulating a bug"""
        with pytest.raises(NotImplementedError):
            main(args=["--debug", "bug", "simulate"])

    def test_bug_list(self) -> None:
        """Tests the functions for listing bugs"""
        bugs.list_bugs()

    @patch("ntclient.services.api.cache_mirrors", return_value="https://someurl.com")
    @patch(
        "ntclient.services.api.ApiClient.post",
        return_value=MagicMock(status_code=201),
    )
    # pylint: disable=unused-argument
    def test_bug_report(self, *args: MagicMock) -> None:
        """Tests the functions for submitting bugs"""
        bugs.submit_bugs()

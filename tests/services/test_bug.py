# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 16:18:08 2024

@author: shane
"""
import unittest

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

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="Work in progress, need to get mocks working")
    def test_bug_report(self) -> None:
        """Tests the functions for submitting bugs"""
        bugs.submit_bugs()

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
        exit_code, _bugs = bugs.list_bugs(show_all=True)

        assert exit_code == 0
        assert len(_bugs) >= 0
        # assert len(rows) >= 0
        # assert len(headers) == 11

    def test_bug_list_unsubmitted(self) -> None:
        """Tests the functions for listing unsubmitted bugs"""
        with patch(
            "ntclient.services.bugs._list_bugs",
            return_value=[{"submitted": False}],
        ):
            exit_code, _bugs = bugs.list_bugs(show_all=False)

        assert exit_code == 0
        assert len(_bugs) == 1
        _bug = _bugs[0]
        assert len(_bug.values()) >= 0
        assert len(_bug.keys()) == 1

    @patch("ntclient.services.api.cache_mirrors", return_value="https://someurl.com")
    @patch(
        "ntclient.services.api.ApiClient.post",
        return_value=MagicMock(status_code=201),
    )
    @patch("ntclient.services.bugs._list_bugs_unsubmitted", return_value=[{"id": 1}])
    @patch("ntclient.services.bugs.sql_nt")
    # pylint: disable=unused-argument
    def test_bug_report(self, *args: MagicMock) -> None:
        """Tests the functions for submitting bugs"""
        bugs.submit_bugs()

    @patch("ntclient.services.api.cache_mirrors", return_value="https://someurl.com")
    @patch(
        "ntclient.services.api.ApiClient.post",
        return_value=MagicMock(status_code=204),
    )
    @patch("ntclient.services.bugs._list_bugs_unsubmitted", return_value=[{"id": 1}])
    @patch("ntclient.services.bugs.sql_nt")
    # pylint: disable=unused-argument
    def test_bug_report_on_204_status(self, *args: MagicMock) -> None:
        """Tests the functions for submitting bugs"""
        bugs.submit_bugs()

    @patch("ntclient.services.api.cache_mirrors", return_value="https://someurl.com")
    @patch(
        "ntclient.services.api.ApiClient.post",
        return_value=MagicMock(status_code=201),
    )
    @patch("ntclient.services.bugs._list_bugs_unsubmitted", return_value=[])
    # pylint: disable=unused-argument
    def test_bug_report_empty_list(self, *args: MagicMock) -> None:
        """Tests the functions for submitting bugs"""
        result = bugs.submit_bugs()
        assert result == 0

# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 16:43:56 2024

@author: shane

NOTE: these tests are in a folder "aaa\" which is alphabetically RUN FIRST.
      Other tests, such as test_bug, depend on having the newer version of nt.sqlite3
"""
from unittest.mock import patch

from ntclient.services import init


def test_init() -> None:
    """Tests the SQL/persistence init in real time"""
    with patch("os.path.isdir", return_value=False):
        with patch("os.makedirs", return_value=None):
            code, result = init(yes=True)

    assert code == 0
    assert result

# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 16:43:56 2024

@author: shane

NOTE: these tests are in a folder "aaa\" which is alphabetically RUN FIRST.
      Other tests, such as test_bug, depend on having the newer version of nt.sqlite3
"""
from ntclient.services import init


def test_init():
    """Tests the SQL/persistence init in real time"""
    code, result = init(yes=True)
    assert code == 0
    assert result

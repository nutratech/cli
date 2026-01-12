# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 18:22:39 2024

@author: shane
"""
import pytest

from ntclient.persistence.sql import _prep_query
from ntclient.persistence.sql.nt import nt_sqlite_connect


def test_prep_query_with_non_iterative_values_throws_type_error() -> None:
    """Test the _prep_query method if a bare (non-iterative) values is passed in."""

    con = nt_sqlite_connect()
    query = "SELECT * FROM version WHERE id = ?;"
    db_name = "nt"
    values = 1

    with pytest.raises(TypeError):
        _prep_query(con, query, db_name, values)  # type: ignore

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 17:30:01 2024

@author: shane
"""
from unittest.mock import patch

import pytest


@patch("sys.version_info", (3, 4, 0))
def test_archaic_python_version_raises_runtime_error() -> None:
    """Test that the correct error is raised when the Python version is too low."""
    with pytest.raises(RuntimeError) as exc_info:
        # pylint: disable=import-outside-toplevel
        from ntclient import PY_MIN_VER, PY_SYS_VER, __title__

        assert __title__ == "nutra"
        assert PY_MIN_VER == (3, 4, 3)
        assert PY_SYS_VER == (3, 4, 0)

    assert "ERROR: nutra requires Python 3.4.3 or later to run" in str(exc_info.value)
    assert "HINT:  You're running Python 3.4.0" in str(exc_info.value)
    assert exc_info.type == RuntimeError
    assert exc_info.value.args == (
        "ERROR: nutra requires Python 3.4.3 or later to run",
        "HINT:  You're running Python 3.4.0",
    )

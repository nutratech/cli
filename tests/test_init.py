# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 17:30:01 2024

@author: shane
"""
from unittest.mock import patch

import pytest

from ntclient import version_check


@patch("sys.version_info", (3, 4, 0))
def test_archaic_python_version_raises_runtime_error() -> None:
    """Test that the correct error is raised when the Python version is too low."""
    with pytest.raises(RuntimeError) as exc_info:
        version_check()

    assert "ERROR: nutra requires Python 3.4.3 or later to run" in str(exc_info.value)
    assert "HINT:  You're running Python 3.4.0" in str(exc_info.value)
    assert exc_info.type == RuntimeError
    assert exc_info.value.args == (
        "ERROR: nutra requires Python 3.4.3 or later to run",
        "HINT:  You're running Python 3.4.0",
    )

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 16:14:03 2024

@author: shane
"""
import unittest

import pytest
import requests_mock as r_mock

from ntclient.services.api import URLS_API, cache_mirrors

if __name__ == "__main__":
    pytest.main()


def test_cache_mirrors(requests_mock: r_mock.Mocker) -> None:
    """Test cache_mirrors"""
    for url in URLS_API:
        requests_mock.get(url, status_code=200)
    assert cache_mirrors() == "https://api.nutra.tk"


def test_cache_mirrors_failing_mirrors_return_empty_string(
    requests_mock: r_mock.Mocker,
) -> None:
    """Test when cache_mirrors are all down, return empty string."""
    for url in URLS_API:
        requests_mock.get(url, status_code=503)
    assert cache_mirrors() == str()

class TestApiClient(unittest.TestCase):
    """Test the ApiClient class."""

        def test_post(self) -> None:
            """Test the post method."""
            with r_mock.Mocker() as m:
                m.post("https://api.nutra.tk/endpoint", status_code=200)
                client = cache_mirrors()
                assert client.post("endpoint", {}) is not None

        def test_post_bug(self) -> None:
            """Test the post_bug method."""
            with r_mock.Mocker() as m:
                m.post("https://api.nutra.tk/endpoint", status_code=200)
                client = cache_mirrors()
                assert client.post_bug({}) is not None
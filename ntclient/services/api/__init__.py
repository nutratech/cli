#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 14:28:20 2024

@author: shane
"""
import sqlite3

import requests

REQUEST_READ_TIMEOUT = 18
REQUEST_CONNECT_TIMEOUT = 5

# TODO: try all of these; cache (save in prefs.json) the one which works first
URLS_API = (
    "https://api.nutra.tk",
    "http://216.218.216.163",  # prod
)


class ApiClient:
    """Client for connecting to the remote server/API."""

    def __init__(
        self,
        host: str = URLS_API[0],
    ):
        self.host = host

    def get(self, path: str) -> requests.Response:
        """Get data from the API."""
        _res = requests.get(
            f"{self.host}/{path}",
            timeout=(REQUEST_CONNECT_TIMEOUT, REQUEST_READ_TIMEOUT),
        )
        _res.raise_for_status()
        return _res

    def post(self, path: str, data: dict) -> requests.Response:
        """Post data to the API."""
        _res = requests.post(
            f"{self.host}/{path}",
            json=data,
            timeout=(REQUEST_CONNECT_TIMEOUT, REQUEST_READ_TIMEOUT),
        )
        _res.raise_for_status()
        return _res

    # TODO: move this outside class; support with host iteration helper method
    def post_bug(self, bug: sqlite3.Row) -> requests.Response:
        """Post a bug report to the developer."""
        return self.post("bug", dict(bug))

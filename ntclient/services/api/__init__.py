#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 14:28:20 2024

@author: shane
"""
import sqlite3

import requests

URL_API = "https://api.nutra.tk"
# TODO: try all of these; cache (save in prefs.json) the one which works first
URLS_API = (
    "https://api.nutra.tk",
    "https://216.218.216.163/api",  # prod
    "https://216.218.228.93/api",  # dev
)
REQUEST_READ_TIMEOUT = 18
REQUEST_CONNECT_TIMEOUT = 5


class ApiClient:
    """Client for connecting to the remote server/API."""

    def __init__(
        self,
        host: str = URL_API,
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
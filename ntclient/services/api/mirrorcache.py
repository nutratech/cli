#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 18:58:12 2024

@author: shane
"""

import requests

from ntclient.services.api import (
    REQUEST_CONNECT_TIMEOUT,
    REQUEST_READ_TIMEOUT,
    URLS_API,
)


def cache_mirrors() -> bool:
    """Cache mirrors"""
    for mirror in URLS_API:
        try:
            _res = requests.get(
                mirror,
                timeout=(REQUEST_CONNECT_TIMEOUT, REQUEST_READ_TIMEOUT),
                verify=mirror.startswith("https://"),
            )

            _res.raise_for_status()
            print(f"INFO: mirror '{mirror}' SUCCEEDED!  Saving it.")
            return True
        except requests.exceptions.ConnectionError:
            print(f"INFO: mirror '{mirror}' failed")

    return False

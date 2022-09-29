# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 14:35:43 2022

@author: shane

Allows the safe avoidance of ImportError on non-colorama capable systems.
Also provides compatibility with old versions of colorama.
"""

# pylint: disable=invalid-name


# pylint: disable=too-few-public-methods
class _STYLE:
    def __init__(self) -> None:
        self.BRIGHT = str()
        self.DIM = str()
        self.RESET_ALL = str()


# pylint: disable=too-few-public-methods,too-many-instance-attributes
class _FORE:
    def __init__(self) -> None:
        self.WARN = str()
        self.CRIT = str()
        self.OVER = str()
        self.DEFAULT = str()

        self.YELLOW = str()
        self.BLUE = str()
        self.RED = str()
        self.MAGENTA = str()

        self.GREEN = str()
        self.CYAN = str()


_Style = _STYLE()
_Fore = _FORE()

try:
    from colorama import Fore, Style
    from colorama import init as colorama_init

    # Made it this far, so run the init function (which is needed on Windows)
    colorama_init()

except ImportError:
    Fore, Style = _Fore, _Style  # type: ignore


# NOTE: These will all just be empty strings if colorama isn't installed
# Styles
STYLE_BRIGHT = Style.BRIGHT
STYLE_DIM = Style.DIM
STYLE_RESET_ALL = Style.RESET_ALL

# Colors for Progress / RDA bar
COLOR_WARN = Fore.YELLOW
COLOR_CRIT = Style.DIM + Fore.RED
COLOR_OVER = Style.DIM + Fore.MAGENTA
COLOR_DEFAULT = Fore.CYAN

# Used in macro bars
COLOR_YELLOW = Fore.YELLOW
COLOR_BLUE = Fore.BLUE
COLOR_RED = Fore.RED

# Used by `tree.py` utility
COLOR_GREEN = Fore.GREEN
COLOR_CYAN = Fore.CYAN

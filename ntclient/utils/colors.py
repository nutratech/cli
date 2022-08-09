# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 14:35:43 2022

@author: shane

Allows the safe avoidance of ImportError on non-colorama capable systems.
"""

try:
    from colorama import Fore, Style
    from colorama import init as colorama_init

    # Made it this far, so run the init function (which is needed on Windows)
    colorama_init()

    COLORAMA_CAPABLE = True

except ImportError:
    COLORAMA_CAPABLE = False


def safe_color(_input_str: str) -> str:
    """Return the colorama value if it exists, otherwise an empty string"""
    return _input_str if COLORAMA_CAPABLE else str()


# NOTE: These will all just be empty strings if colorama isn't installed
# Styles
STYLE_BRIGHT = safe_color(Style.BRIGHT)
STYLE_DIM = safe_color(Style.DIM)
STYLE_RESET_ALL = safe_color(Style.RESET_ALL)

# Colors
COLOR_WARN = safe_color(Fore.YELLOW)
COLOR_CRIT = safe_color(Style.DIM + Fore.RED)
COLOR_OVER = safe_color(Style.DIM + Fore.MAGENTA)

COLOR_DEFAULT = safe_color(Fore.CYAN)

# Used in macro bars
COLOR_YELLOW = safe_color(Fore.YELLOW)
COLOR_BLUE = safe_color(Fore.BLUE)
COLOR_RED = safe_color(Fore.RED)

# Used by `tree.py` utility
COLOR_GREEN = safe_color(Fore.GREEN)
COLOR_CYAN = safe_color(Fore.CYAN)

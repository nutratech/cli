#!/usr/bin/env python3
"""Python 3 reimplementation of the linux 'tree' utility"""

import os
import sys

from colorama import Fore, Style

chars = {"nw": "\u2514", "nws": "\u251c", "ew": "\u2500", "ns": "\u2502"}

strs = [
    chars["ns"] + "   ",
    chars["nws"] + chars["ew"] * 2 + " ",
    chars["nw"] + chars["ew"] * 2 + " ",
    "    ",
]

# Colors and termination strings
COLOR_DIR = Style.BRIGHT + Fore.BLUE
COLOR_EXEC = Style.BRIGHT + Fore.GREEN
COLOR_LINK = Style.BRIGHT + Fore.CYAN
COLOR_DEAD_LINK = Style.BRIGHT + Fore.RED


def colorize(path: str, full: bool = False) -> str:
    """Returns string with color / bold"""
    file = path if full else os.path.basename(path)

    if os.path.islink(path):
        return "".join(
            [
                COLOR_LINK,
                file,
                Style.RESET_ALL,
                " -> ",
                colorize(os.readlink(path), True),
            ]
        )

    if os.path.isdir(path):
        return "".join([COLOR_DIR, file, Style.RESET_ALL])

    if os.access(path, os.X_OK):
        return "".join([COLOR_EXEC, file, Style.RESET_ALL])

    return file


def print_dir(_dir: str, pre: str = str(), opts: dict = None) -> tuple:
    """Prints the whole tree"""
    n_dirs = 0
    n_files = 0
    n_size = 0

    if not opts:
        opts = {}

    if not pre:
        print(COLOR_DIR + _dir + Style.RESET_ALL)

    dir_len = len(os.listdir(_dir)) - 1
    for i, file in enumerate(sorted(os.listdir(_dir), key=str.lower)):
        path = os.path.join(_dir, file)
        if file[0] == "." and not opts["show_hidden"]:
            continue
        if os.path.isdir(path):
            print(pre + strs[2 if i == dir_len else 1] + colorize(path))
            if os.path.islink(path):
                n_dirs += 1
            else:
                n_d, n_f, n_s = print_dir(
                    path, pre + strs[3 if i == dir_len else 0], opts=opts
                )
                n_dirs += n_d + 1
                n_files += n_f
                n_size += n_s
        else:
            n_files += 1
            n_size += os.path.getsize(path)
            print(
                pre
                + strs[2 if i == dir_len else 1]
                + ("[{:>11}]  ".format(n_size) if opts["show_size"] else "")
                + colorize(path)
            )

    return (n_dirs, n_files, n_size)


def main() -> int:
    """Handle input arguments, print off tree"""
    n_dirs = 0
    n_files = 0

    opts = {"show_hidden": False, "show_size": False, "follow_symlinks": False}

    if len(sys.argv) == 1:
        n_dirs, n_files, _size = print_dir(".", opts=opts)
    else:
        for _dir in sys.argv[1:]:
            n_d, n_f, _size = print_dir(_dir, opts=opts)
            n_dirs += n_d
            n_files += n_f

    print()
    print(
        "{} director{}, {} file{}".format(
            n_dirs, "ies" if n_dirs != 1 else "y", n_files, "s" if n_files != 1 else ""
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Custom types for argparse validation"""
import argparse
import os


def file_path(path_in: str) -> str:
    """Returns file if it exists, else raises argparse error"""
    if os.path.isfile(path_in):
        return path_in
    raise argparse.ArgumentTypeError('FileNotFoundError: "%s"' % path_in)


def file_or_dir_path(path_in: str) -> str:
    """Returns path if it exists, else raises argparse error"""
    if os.path.exists(path_in):
        return path_in
    raise argparse.ArgumentTypeError('FileNotFoundError: "%s"' % path_in)

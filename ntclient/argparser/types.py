"""Custom types for argparse validation"""
import argparse
import os


def file_path(string):
    """Returns file if it exists, else raises argparse error"""
    if os.path.isfile(string):
        return string
    raise argparse.ArgumentTypeError('FileNotFoundError: "%s"' % string)


def file_or_dir_path(string):
    """Returns path if it exists, else raises argparse error"""
    if os.path.exists(string):
        return string
    raise argparse.ArgumentTypeError('FileNotFoundError: "%s"' % string)

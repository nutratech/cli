# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 15:34:07 2022

@author: shane
Classes, structures for storing, displaying, and editing data.
"""


class Recipe:
    """Allows"""

    def __init__(self, file_path: str) -> None:
        """Initialize entity"""

        self.file_path = file_path
        with open(file_path, "r", encoding="utf-8") as _file:
            self.raw_data = _file.readlines()

        # Defined now, populated later
        self.rows: list = []

    def process_data(self) -> None:
        """Parses out the raw CSV input read in during self.__init__()"""
        self.rows = [x.rstrip() for x in self.raw_data]

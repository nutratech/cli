# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 15:34:07 2022

@author: shane
Classes, structures for storing, displaying, and editing data.
"""
import csv


class Recipe:
    """Allows reading up CSV, filtering by UUID, and displaying detail view"""

    def __init__(self, file_path: str) -> None:
        """Initialize entity"""

        self.file_path = file_path
        self.csv_reader = csv.reader(str())

        # Defined now, populated later
        self.headers = tuple()  # type: ignore
        self.rows = tuple()  # type: ignore

        self.uuid = str()

    def process_data(self) -> None:
        """Parses out the raw CSV input read in during self.__init__()"""

        # Read into memory
        with open(self.file_path, "r", encoding="utf-8") as _file:
            self.csv_reader = csv.DictReader(_file)
            _rows = tuple(self.csv_reader)
            self.headers = tuple(_rows[0])
            self.rows = tuple(_rows[1:])

        # Validate data
        uuids = {x for x in self.rows}

        print("hi")

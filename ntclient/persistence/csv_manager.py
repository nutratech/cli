"""
CSV Persistence Manager
Handles reading and writing to daily log CSV files.
"""

import csv
import os
from typing import Dict, List, Union


def ensure_log_exists(log_path: str) -> None:
    """Creates the log file with headers if it doesn't exist."""
    if not os.path.exists(log_path):
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "grams"])


def append_to_log(log_path: str, food_id: int, grams: float) -> None:
    """Appends a food entry to the specified log file."""
    ensure_log_exists(log_path)
    with open(log_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([food_id, grams])


def read_log(log_path: str) -> List[Dict[str, Union[str, float]]]:
    """Reads a log file and returns a list of dictionaries."""
    if not os.path.exists(log_path):
        return []

    with open(log_path, "r", encoding="utf-8") as f:
        # Filter out comments/empty lines if necessary, matching existing logic
        rows = [row for row in f if not row.startswith("#") and row.strip()]
        if not rows:
            return []

        reader = csv.DictReader(rows)
        # Check if empty (headers only or truly empty) - DictReader handles headers
        return list(reader)

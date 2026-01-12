"""
Logs Service
Business logic for managing daily food logs.
"""

import datetime
import os
from typing import Optional

from tabulate import tabulate

from ntclient import NUTRA_HOME
from ntclient.persistence.csv_manager import append_to_log, read_log
from ntclient.persistence.sql.usda.funcs import sql_food_details
from ntclient.services.analyze import day_analyze


def get_log_path(date_str: Optional[str] = None) -> str:
    """
    Returns the absolute path to the log file for the given date.
    Defaults to today's date if date_str is None.
    Expected date format: YYYY-MM-DD (or similar valid filename)
    """
    if not date_str:
        date_str = datetime.date.today().isoformat()

    # Sanitize inputs strictly if necessary, but assuming basic CLI usage for now
    filename = f"{date_str}.csv"
    return os.path.join(NUTRA_HOME, filename)


def log_add(food_id: int, grams: float, date_str: Optional[str] = None) -> None:
    """
    Adds a food entry to the recurring daily log.
    Validates that the food_id exists in the USDA database.
    """
    # Validate Food ID
    food_details = sql_food_details({food_id})
    if not food_details:
        print(f"ERROR: Food ID {food_id} not found in database.")
        return

    log_path = get_log_path(date_str)
    append_to_log(log_path, food_id, grams)

    # Feedback
    food_name = food_details[0][2]
    # Truncate
    if len(food_name) > 40:
        food_name = food_name[:37] + "..."
    print(
        f"Added: {grams}g of '{food_name}' ({food_id}) to {os.path.basename(log_path)}"
    )


def log_view(date_str: Optional[str] = None) -> None:
    """
    Views the raw entries of a log file.
    """
    log_path = get_log_path(date_str)
    entries = read_log(log_path)

    if not entries:
        print(f"No log entries found for {os.path.basename(log_path)}")
        return

    # Enrich with food names for display
    # entries is list of dicts like {'id': '1001', 'grams': '100'}
    food_ids = {int(e["id"]) for e in entries if e["id"]}
    food_des = {x[0]: x[2] for x in sql_food_details(food_ids)}

    table_data = []
    for e in entries:
        fid = int(e["id"])
        grams = float(e["grams"])
        name = food_des.get(fid, "Unknown Food")
        if len(name) > 50:
            name = name[:47] + "..."
        table_data.append([fid, name, grams])

    print(f"\nLog: {os.path.basename(log_path)}")
    print(tabulate(table_data, headers=["ID", "Food", "Grams"], tablefmt="simple"))


def log_analyze(date_str: Optional[str] = None) -> None:
    """
    Runs full analysis on the log file.
    """
    log_path = get_log_path(date_str)
    if not os.path.exists(log_path):
        print(f"Log file not found: {log_path}")
        return

    # Reuse existing analysis logic
    day_analyze([log_path])

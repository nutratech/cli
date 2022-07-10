"""Biometrics SQL functions"""
from tabulate import tabulate

from ntclient.persistence import PROFILE_ID
from ntclient.persistence.sql.nt.funcs import (
    sql_biometric_add,
    sql_biometric_logs,
    sql_biometrics,
)


def biometrics():
    """Shows biometrics"""
    headers, rows = sql_biometrics()
    table = tabulate(rows, headers=headers, tablefmt="presto")
    print(table)
    return 0, rows


def biometric_logs():
    """Shows biometric logs"""
    headers, rows = sql_biometric_logs(PROFILE_ID)

    table = tabulate(rows, headers=headers, tablefmt="presto")
    print(table)
    return 0, rows


def biometric_add(bio_vals):
    """Add a biometric type"""
    print()
    # print("New biometric log: " + name + "\n")

    bio_names = {x[0]: x for x in sql_biometrics()[1]}

    results = []
    for biometric_id, value in bio_vals.items():
        bio = bio_names[biometric_id]
        results.append(
            {"id": biometric_id, "name": bio[1], "value": value, "unit": bio[2]}
        )

    table = tabulate(results, headers="keys", tablefmt="presto")
    print(table)

    # TODO: print current profile and date?

    confirm = input("\nConfirm add biometric? [Y/n] ")

    if confirm.lower() == "y":
        sql_biometric_add(bio_vals)
        print("not implemented ;]")
    return 1, False

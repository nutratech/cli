"""Main SQL persistence module, need to rethink circular imports and shared code"""
import sqlite3
from typing import Union

# FIXME: maybe just use separate methods for calls with vs. without headers
#  avoid the mypy headaches, and the liberal comments  # type: ignore


def sql_entries(sql_result: sqlite3.Cursor, headers=False) -> Union[list, tuple]:
    """Formats and returns a `sql_result()` for console digestion and output"""
    # TODO: return object: metadata, command, status, errors, etc?
    rows = sql_result.fetchall()

    if headers:
        headers = [x[0] for x in sql_result.description]
        return headers, rows

    return rows


def version(con: sqlite3.Connection) -> str:
    """Gets the latest entry from version table"""

    cur = con.cursor()
    result = cur.execute("SELECT * FROM version;").fetchall()
    close_con_and_cur(con, cur, commit=False)
    return result[-1][1]


def close_con_and_cur(
    con: sqlite3.Connection, cur: sqlite3.Cursor, commit=True
) -> None:
    """Cleans up, commits, and closes after an SQL command is run"""

    cur.close()
    if commit:
        con.commit()
    con.close()


def _sql(
    con: sqlite3.Connection,
    query: str,
    db_name: str,
    values: Union[tuple, list] = None,
    headers=False,
) -> Union[list, tuple]:
    from ntclient import DEBUG  # pylint: disable=import-outside-toplevel

    cur = con.cursor()

    if DEBUG:
        print("%s.sqlite3: %s" % (db_name, query))
        if values:
            # TODO: better debug logging, more "control-findable", distinguish from most prints()
            print(values)

    # TODO: separate `entry` & `entries` entity for single vs. bulk insert?
    if values:
        if isinstance(values, list):
            rows = cur.executemany(query, values)
        else:  # tuple
            rows = cur.execute(query, values)
    else:
        rows = cur.execute(query)

    # TODO: print "<number> SELECTED", or other info BASED ON command SELECT/INSERT/DELETE/UPDATE
    result = sql_entries(rows, headers=headers)
    close_con_and_cur(con, cur)
    return result

"""nt.sqlite3 functions module"""
from ntclient.persistence import PROFILE_ID
from ntclient.persistence.sql.nt import nt_sqlite_connect, sql


def sql_nt_next_index(table=None):
    """Used for previewing inserts"""
    query = "SELECT MAX(id) FROM %s;" % table  # nosec: B608
    return int(sql(query)[0]["MAX(id)"])


################################################################################
# Recipe functions
################################################################################
def sql_recipe(recipe_id):
    """Selects columns for recipe_id"""
    query = "SELECT * FROM recipes WHERE id=?;"
    return sql(query, values=(recipe_id,))


def sql_recipes():
    """Show recipes with selected details"""
    query = """
SELECT
  id,
  tagname,
  name,
  COUNT(recipe_id) AS n_foods,
  SUM(grams) AS grams,
  created
FROM
  recipes
  LEFT JOIN recipe_dat ON recipe_id = id
GROUP BY
  id;
"""
    return sql(query, headers=True)


def sql_analyze_recipe(recipe_id):
    """Output (nutrient) analysis columns for a given recipe_id"""
    query = """
SELECT
  id,
  name,
  food_id,
  grams
FROM
  recipes
  INNER JOIN recipe_dat ON recipe_id = id
    AND id = ?;
"""
    return sql(query, values=(recipe_id,))


def sql_recipe_add():
    """TODO: method for adding recipe"""
    query = """
"""
    return sql(query)


################################################################################
# Biometric functions
################################################################################
def sql_biometrics():
    """Selects biometrics"""
    query = "SELECT * FROM biometrics;"
    return sql(query, headers=True)


def sql_biometric_logs(profile_id):
    """Selects biometric logs"""
    query = "SELECT * FROM biometric_log WHERE profile_id=?"
    return sql(query, values=(profile_id,), headers=True)


def sql_biometric_add(bio_vals):
    """Insert biometric log item"""
    con = nt_sqlite_connect()
    cur = con.cursor()

    # TODO: finish up
    query1 = "INSERT INTO biometric_log(profile_id, tags, notes) VALUES (?, ?, ?)"
    sql(query1, (PROFILE_ID, "", ""))
    log_id = cur.lastrowid
    print(log_id)
    query2 = "INSERT INTO bio_log_entry(log_id, biometric_id, value) VALUES (?, ?, ?)"
    records = [
        (log_id, biometric_id, value) for biometric_id, value in bio_vals.items()
    ]
    cur.executemany(query2, records)
    return log_id

"""nt.sqlite3 functions module"""
from ntclient.persistence.sql.nt import sql, sql_headers


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
    return sql_headers(query)


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

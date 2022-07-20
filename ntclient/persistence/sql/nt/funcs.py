"""nt.sqlite3 functions module"""
from ntclient.persistence.sql.nt import sql, sql_headers


def sql_nt_next_index(table: str) -> int:
    """Used for previewing inserts"""
    # noinspection SqlResolve
    query = "SELECT MAX(id) as max_id FROM %s;" % table  # nosec: B608
    return int(sql(query)[0]["max_id"])


################################################################################
# Recipe functions
################################################################################
def sql_recipe(recipe_id: int) -> list:
    """Selects columns for recipe_id"""
    query = "SELECT * FROM recipe WHERE id=?;"
    return sql(query, values=(recipe_id,))


def sql_recipes() -> tuple:
    """Show recipes with selected details"""
    query = """
SELECT
  id,
  tagname,
  name,
  COUNT(recipe_id) AS n_foods,
  SUM(grams) AS grams,
  recipe.created as created
FROM
  recipe
  LEFT JOIN recipe_dat ON recipe_id = id
GROUP BY
  id;
"""
    return sql_headers(query)


def sql_analyze_recipe(recipe_id: int) -> list:
    """Output (nutrient) analysis columns for a given recipe_id"""
    query = """
SELECT
  id,
  name,
  food_id,
  grams
FROM
  recipe
  INNER JOIN recipe_dat ON recipe_id = id
    AND id = ?;
"""
    return sql(query, values=(recipe_id,))


def sql_recipe_add() -> list:
    """TODO: method for adding recipe"""
    query = """
"""
    return sql(query)

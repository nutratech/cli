# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 19:43:55 2020

@author: shane
"""


# pylint: disable=too-few-public-methods
class Nutrient:
    """Tracks properties of nutrients; used in the tree structure of nutrient groups"""

    def __init__(self, nut_id: int, name: str, hidden: bool = False):
        self.nut_id = nut_id
        self.name = name
        self.hidden = hidden


nnest = {
    # "basics": ["Protein", "Carbs", "Fats", "Fiber", "Calories"],
    "basics": {
        # 203: {"name": "Protein", "hidden": False},
        203: Nutrient(203, "Protein"),
        205: "Carbs",
        204: "Fats",
        291: "Fiber",
        208: "Calories (kcal)",
    },
    "macro_details": {"Carbs": {}, "Fat": {}},
    "micro_nutrients": {
        "Vitamins": {"Water-Soluble": {}, "Fat-Soluble": {}},
        "Minerals": [],
    },
    "fatty_acids": {},
    "amino_acids": set(),
    "other_components": {},
}

"""
from ChatGPT:


Here are the grouped categories and sub-categories of related nutrients based on the
provided table:

1. Protein:
   - Protein (203)

2. Fat:
   - Total lipid (fat) (204)
   - Fatty acids:
     - Total trans (605)
     - Total saturated (606)
     - Total monounsaturated (645)
     - Total polyunsaturated (646)

3. Carbohydrates:
   - Carbohydrate, by difference (205)
   - Sugars:
     - Sucrose (210)
     - Glucose (dextrose) (211)
     - Fructose (212)
     - Lactose (213)
     - Maltose (214)
     - Sugars, total (269)
   - Starch (209)
   - Fiber, total dietary (291)

4. Minerals:
   - Electrolytes:
     - Potassium, K (306)
     - Sodium, Na (307)
     - Magnesium, Mg (304)
     - Calcium, Ca (301)
   - Iron, Fe (303)
   - Phosphorus, P (305)
   - Zinc, Zn (309)
   - Copper, Cu (312)
   - Fluoride, F (313)
   - Manganese, Mn (315)
   - Selenium, Se (317)

5. Vitamins:
   - Vitamin A:
     - Vitamin A, IU (318)
     - Retinol (319)
     - Vitamin A, RAE (320)
     - Carotene:
       - Carotene, beta (321)
       - Carotene, alpha (322)
   - Vitamin E:
     - Vitamin E (alpha-tocopherol) (323)
     - Vitamin E, added (573)
   - Vitamin D:
     - Vitamin D (324)
     - Vitamin D2 (ergocalciferol) (325)
     - Vitamin D3 (cholecalciferol) (326)
     - Vitamin D (D2 + D3) (328)
   - Vitamin C:
     - Vitamin C, total ascorbic acid (401)
   - B Vitamins:
     - Thiamin (404)
     - Riboflavin (405)
     - Niacin (406)
     - Pantothenic acid (410)
     - Vitamin B-6 (415)
     - Folate:
       - Folate, total (417)
       - Folic acid (431)
       - Folate, food (432)
       - Folate, DFE (435)
     - Vitamin B-12:
       - Vitamin B-12 (418)
       - Vitamin B-12, added (578)
     - Choline, total (421)
   - Vitamin K:
     - Vitamin K (phylloquinone) (430)

6. Other Organic Compounds:
   - Water (255)
   - Caffeine (262)
   - Theobromine (263)
   - Betaine (454)
   - Cholesterol (601)
   - Phytosterols:
     - Phytosterols (636)
     - Stigmasterol (638)
     - Campesterol (639)
     - Beta-sitosterol (641)
   - Phytochemicals (e.g., flavonoids, isoflavones) and their subcategories
   - Ash (207)

Please note that this list may not include all possible nutrient categories and
sub-categories, and there may be other ways to categorize them as well.
"""

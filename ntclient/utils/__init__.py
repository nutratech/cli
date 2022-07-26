"""Constants and default settings"""
from enum import Enum

from colorama import Fore, Style

################################################################################
# Colors and buffer settings
################################################################################

# TODO: make configurable in SQLite or prefs.json

THRESH_WARN = 0.7
COLOR_WARN = Fore.YELLOW

THRESH_CRIT = 0.4
COLOR_CRIT = Style.DIM + Fore.RED

THRESH_OVER = 1.9
COLOR_OVER = Style.DIM + Fore.MAGENTA

COLOR_DEFAULT = Fore.CYAN

################################################################################
# Nutrient IDs
################################################################################
NUTR_ID_KCAL = 208

NUTR_ID_PROTEIN = 203

NUTR_ID_CARBS = 205
NUTR_ID_SUGAR = 269
NUTR_ID_FIBER = 291

NUTR_ID_FAT_TOT = 204
NUTR_ID_FAT_SAT = 606
NUTR_ID_FAT_MONO = 645
NUTR_ID_FAT_POLY = 646

NUTR_IDS_FLAVONES = [
    710,
    711,
    712,
    713,
    714,
    715,
    716,
    734,
    735,
    736,
    737,
    738,
    731,
    740,
    741,
    742,
    743,
    745,
    749,
    750,
    751,
    752,
    753,
    755,
    756,
    758,
    759,
    762,
    770,
    773,
    785,
    786,
    788,
    789,
    791,
    792,
    793,
    794,
]

NUTR_IDS_AMINOS = [
    501,
    502,
    503,
    504,
    505,
    506,
    507,
    508,
    509,
    510,
    511,
    512,
    513,
    514,
    515,
    516,
    517,
    518,
    521,
]


################################################################################
# Enums
################################################################################
class Gender(Enum):
    """
    A validator and Enum class for gender inputs; used in several calculations.
    @note: floating point -1 to 1, or 0 to 1... for non-binary?
    """

    MALE = "m"
    FEMALE = "f"


class ActivityFactor(Enum):
    """
    Used in BMR calculations.
    Different activity levels: {0.200, 0.375, 0.550, 0.725, 0.900}
    @todo: Verify the accuracy of these "names". Access by index?
    """

    SEDENTARY = {1: 0.2}
    MILDLY_ACTIVE = {2: 0.375}
    ACTIVE = {3: 0.55}
    HIGHLY_ACTIVE = {4: 0.725}
    INTENSELY_ACTIVE = {5: 0.9}


def activity_factor_from_float(activity_factor: int) -> float:
    """
    Gets ActivityFactor Enum by float value if it exists, else raise ValueError.
    Basically just verifies the float is among the allowed values, and re-returns it.
    """
    for enum_entry in ActivityFactor:
        if activity_factor in enum_entry.value:
            return float(enum_entry.value[activity_factor])
    # TODO: custom exception. And handle in main file?
    raise ValueError("No such ActivityFactor for value: %s" % activity_factor)

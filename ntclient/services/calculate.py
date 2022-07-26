# -*- coding: utf-8 -*-
"""
Calculate service for one rep max, BMR, body fat.

Created on Tue Aug 11 20:53:14 2020

@author: shane
"""
import argparse
import math
from datetime import datetime

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 1 rep max
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from ntclient import Gender, activity_factor_from_index

common_n_reps = (1, 2, 3, 5, 6, 8, 10, 12, 15, 20)


def orm_epley(reps: float, weight: float) -> dict:
    """
    Returns a dict {n_reps: max_weight, ...}
        for n_reps: (1, 2, 3, 5, 6, 8, 10, 12, 15, 20)

    1 RM = weight * (1 + (reps - 1) / 30)

    Source: https://workoutable.com/one-rep-max-calculator/
    """

    def one_rm() -> float:
        _un_rounded_result = weight * (1 + (reps - 1) / 30)
        return round(_un_rounded_result, 1)

    def weight_max_reps(target_reps: float) -> float:
        _un_rounded_result = one_rm() / (1 + (target_reps - 1) / 30)
        return round(_un_rounded_result, 1)

    maxes = {n_reps: weight_max_reps(n_reps) for n_reps in common_n_reps}
    return maxes


def orm_brzycki(reps: float, weight: float) -> dict:
    """
    Returns a dict {n_reps: max_weight, ...}
        for n_reps: (1, 2, 3, 5, 6, 8, 10, 12, 15)

    1 RM = weight * 36 / (37 - reps)

    Source: https://workoutable.com/one-rep-max-calculator/
    """

    def _one_rm() -> float:
        _un_rounded_result = weight * 36 / (37 - reps)
        return round(_un_rounded_result, 1)

    one_rm = _one_rm()

    def weight_max_reps(target_reps: float) -> float:
        _un_rounded_result = one_rm / (1 + (target_reps - 1) / 30)
        return round(_un_rounded_result, 1)

    maxes = {n_reps: weight_max_reps(n_reps) for n_reps in common_n_reps}
    return maxes


def orm_dos_remedios(reps: int, weight: float) -> dict:
    """
    Returns dict {n_reps: max_weight, ...}
        for n_reps: (1, 2, 3, 5, 6, 8, 10, 12, 15)

    Or an {"errMsg": "INVALID_RANGE", ...}

    Source:
        https://www.peterrobertscoaching.com/blog/the-best-way-to-calculate-1-rep-max
    """

    _common_n_reps = {
        1: 1,
        2: 0.92,
        3: 0.9,
        5: 0.87,
        6: 0.82,
        8: 0.75,
        10: 0.7,
        12: 0.65,
        15: 0.6,
    }

    def _one_rm() -> float:
        _multiplier = _common_n_reps[reps]
        _un_rounded_result = weight / _multiplier
        return round(_un_rounded_result, 1)

    try:
        one_rm = _one_rm()
    except KeyError:
        # _logger.debug(traceback.format_exc())
        valid_reps = list(_common_n_reps.keys())
        return {
            "errMsg": "INVALID_RANGE — "
            + f"requires: reps in {valid_reps}, got {reps}",
        }

    def max_weight(target_reps: int) -> float:
        _multiplier = _common_n_reps[target_reps]
        _un_rounded_result = one_rm * _multiplier
        return round(_un_rounded_result, 1)

    return {n_reps: max_weight(n_reps) for n_reps in _common_n_reps}


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# BMR
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def bmr_katch_mcardle(lbm: float, _activity_factor: int) -> dict:
    """
    @param lbm: lean mass in kg
    @param _activity_factor: {0.200, 0.375, 0.550, 0.725, 0.900}

    BMR = 370 + (21.6 x Lean Body Mass(kg) )

    Source: https://www.calculatorpro.com/calculator/katch-mcardle-bmr-calculator/
    Source: https://tdeecalculator.net/about.php
    """
    # Validate it conforms to one of the enum values
    # TODO: return 400s in cases like this, not 500
    # NOTE: is this necessary if it's also done in the controller?
    activity_factor = activity_factor_from_index(_activity_factor)

    bmr = 370 + (21.6 * lbm)
    tdee = bmr * (1 + activity_factor)

    return {
        "bmr": round(bmr),
        "tdee": round(tdee),
    }


def bmr_cunningham(lbm: float, _activity_factor: int) -> dict:
    """
    @param lbm: lean mass in kg
    @param _activity_factor: {0.200, 0.375, 0.550, 0.725, 0.900}

    Source: https://www.slideshare.net/lsandon/weight-management-in-athletes-lecture
    """
    activity_factor = activity_factor_from_index(_activity_factor)

    bmr = 500 + 22 * lbm
    tdee = bmr * (1 + activity_factor)

    return {
        "bmr": round(bmr),
        "tdee": round(tdee),
    }


def bmr_mifflin_st_jeor(
    gender: Gender, weight: float, height: float, dob: int, _activity_factor: int
) -> dict:
    """
    @param gender: {'MALE', 'FEMALE'}
    @param weight: kg
    @param height: cm
    @param dob: int, unix timestamp (seconds)
    @param _activity_factor: {0.200, 0.375, 0.550, 0.725, 0.900}

    Activity Factor\n
    ---------------\n
    0.200 = sedentary (little or no exercise)

    0.375 = lightly active
        (light exercise/sports 1-3 days/week, approx. 590 Cal/day)

    0.550 = moderately active
        (moderate exercise/sports 3-5 days/week, approx. 870 Cal/day)

    0.725 = very active
        (hard exercise/sports 6-7 days a week, approx. 1150 Cal/day)

    0.900 = extra active
        (very hard exercise/sports and physical job, approx. 1580 Cal/day)

    Source: https://www.myfeetinmotion.com/mifflin-st-jeor-equation/
    """
    activity_factor = activity_factor_from_index(_activity_factor)

    def gender_specific_bmr(_gender: Gender, _bmr: float) -> float:
        _second_term = {
            Gender.MALE: 5,
            Gender.FEMALE: -161,
        }
        return _bmr + _second_term[_gender]

    bmr = 10 * weight + 6.25 + 6.25 * height - 5 * _age(dob)

    bmr = gender_specific_bmr(gender, bmr)
    tdee = bmr * (1 + activity_factor)

    return {
        "bmr": round(bmr),
        "tdee": round(tdee),
    }


def bmr_harris_benedict(
    gender: Gender, weight: float, height: float, dob: int, _activity_factor: int
) -> dict:
    """
    @param gender: MALE, FEMALE
    @param weight: kg
    @param height: cm
    @param dob: int, unix timestamp (seconds)
    @param _activity_factor: {0.200, 0.375, 0.550, 0.725, 0.900}

    Harris-Benedict = (13.397m + 4.799h - 5.677a) + 88.362 (MEN)

    Harris-Benedict = (9.247m + 3.098h - 4.330a) + 447.593 (WOMEN)

    m: mass (kg), h: height (cm), a: age (years)

    Source: https://tdeecalculator.net/about.php
    """
    activity_factor = activity_factor_from_index(_activity_factor)

    def gender_specific_bmr(_gender: Gender) -> float:
        age = _age(dob)

        _gender_specific_bmr = {
            Gender.MALE: (13.397 * weight + 4.799 * height - 5.677 * age) + 88.362,
            Gender.FEMALE: (9.247 * weight + 3.098 * height - 4.330 * age) + 447.593,
        }
        return _gender_specific_bmr[_gender]

    bmr = gender_specific_bmr(gender)
    tdee = bmr * (1 + activity_factor)

    return {
        "bmr": round(bmr),
        "tdee": round(tdee),
    }


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Body fat
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def bf_navy(gender: Gender, args: argparse.Namespace) -> float:
    """
    @param gender: MALE or FEMALE
    @param args: argparse namespace dict containing:
        height, waist, neck, and (if female) hip.
        All values are in cm.

    @return: float (e.g. 0.17)

    Source:
        https://www.thecalculator.co/health/Navy-Method-Body-Fat-Measurement-Calculator-1112.html
    """

    # Navy values
    height = float(args.height)
    print()
    print("Height: %s cm" % height)

    waist = float(args.waist)
    print("Waist: %s cm" % waist)
    if gender == Gender.FEMALE:
        hip = float(args.hip)
        print("Hip: %s cm" % hip)
    else:
        hip = 0.0  # placeholder value, not used for men anyway
    neck = float(args.neck)
    print("Neck: %s cm" % neck)

    # Compute values
    _gender_specific_denominator = {
        Gender.MALE: (
            1.0324 - 0.19077 * math.log10(waist - neck) + 0.15456 * math.log10(height)
        ),
        Gender.FEMALE: (
            1.29579
            - 0.35004 * math.log10(waist + hip - neck)
            + 0.22100 * math.log10(height)
        ),
    }

    return round(495 / _gender_specific_denominator[gender] - 450, 2)


def bf_3site(gender: Gender, args: argparse.Namespace) -> float:
    """
    @param gender: MALE or FEMALE
    @param args: dict containing age, and skin manifolds (mm) for
        chest, abdominal, and thigh.

    @return: float (e.g. 0.17)

    Source:
        https://www.thecalculator.co/health/Body-Fat-Percentage-3-Site-Skinfold-Test-1113.html
    """

    # Shared parameters for skin manifold 3 & 7 site tests
    age = float(args.age)
    print()
    print("Age: %s years" % age)

    # 3-Site values
    chest = int(args.chest)
    print("Chest: %s mm" % chest)
    abd = int(args.abd)
    print("Abdominal: %s mm" % abd)
    thigh = int(args.thigh)
    print("Thigh: %s mm" % thigh)

    # Compute values
    st3 = chest + abd + thigh
    _gender_specific_denominator = {
        Gender.MALE: 1.10938
        - 0.0008267 * st3
        + 0.0000016 * st3 * st3
        - 0.0002574 * age,
        Gender.FEMALE: 1.089733
        - 0.0009245 * st3
        + 0.0000025 * st3 * st3
        - 0.0000979 * age,
    }

    return round(495 / _gender_specific_denominator[gender] - 450, 2)


def bf_7site(gender: Gender, args: argparse.Namespace) -> float:
    """
    @param gender: MALE or FEMALE
    @param args: dict containing age, and skin manifolds (mm) for
        chest, abdominal, thigh, triceps, sub, sup, and mid.

    @return: float (e.g. 0.17)

    Source:
        https://www.thecalculator.co/health/Body-Fat-Percentage-7-Site-Skinfold-Calculator-1115.html
    """

    # Shared parameters for skin manifold 3 & 7 site tests
    age = float(args.age)

    # 3-Site values
    chest = int(args.chest)
    abd = int(args.abd)
    thigh = int(args.thigh)

    # 7-Site values
    tricep = int(args.tricep)
    print()
    print("Tricep: %s mm" % tricep)
    sub = int(args.sub)
    print("Sub: %s mm" % sub)
    sup = int(args.sup)
    print("Sup: %s mm" % sup)
    mid = int(args.mid)
    print("Mid: %s mm" % mid)

    # Compute values
    st7 = chest + abd + thigh + tricep + sub + sup + mid

    _gender_specific_denominator = {
        Gender.MALE: 1.112
        - 0.00043499 * st7
        + 0.00000055 * st7 * st7
        - 0.00028826 * age,
        Gender.FEMALE: 1.097
        - 0.00046971 * st7
        + 0.00000056 * st7 * st7
        - 0.00012828 * age,
    }

    return round(495 / _gender_specific_denominator[gender] - 450, 2)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Misc functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def _age(dob: int) -> float:
    """
    Calculate age based on birthday.

    @param dob: birth time in UNIX seconds
    @return: age in years
    """
    now = datetime.now().timestamp()
    years = (now - dob) / (365 * 24 * 3600)
    return years

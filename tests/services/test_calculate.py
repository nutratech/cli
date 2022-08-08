# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 12:13:01 2022

@author: shane

Tests the "calculate service" for any anomalies.
"""
import pytest

import ntclient.services.calculate as calc


@pytest.mark.parametrize("_eq", ["epley", "brzycki", "dos_remedios"])
@pytest.mark.parametrize(
    "weight,reps",
    [
        (50.0, 1),
        (50.0, 2),
        (50.0, 3),
        (50.0, 5),
        (50.0, 6),
        (50.0, 8),
        (50.0, 10),
        (50.0, 12),
        (50.0, 15),
        (50.0, 20),
    ],
)
def test_000_orm_same_in_same_out(_eq: str, weight: float, reps: int) -> None:
    """Test one rep max: Epley"""
    if _eq == "epley":
        result = calc.orm_epley(weight, reps)

    elif _eq == "brzycki":
        result = calc.orm_brzycki(weight, reps)

    else:  # _eq == "dos_remedios"
        result = calc.orm_dos_remedios(weight, reps)

    try:
        # Check results
        assert result[reps] == weight
    except KeyError:
        # dose Remedios does not work for 20 reps currently
        assert _eq == "dos_remedios"
        assert reps == 20

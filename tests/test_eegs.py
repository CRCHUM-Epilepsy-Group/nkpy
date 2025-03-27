from __future__ import annotations

from datetime import datetime
from pathlib import Path
from random import shuffle

import pytest

import nkpy
from nkpy.excel import EEGFile, Patient


@pytest.fixture
def eegs() -> list[EEGFile]:
    eegs = [
        EEGFile(
            path=Path(),
            start=datetime(2024, 1, 1, hour, 0, 0),
            end=datetime(2024, 1, 1, hour, 59, 0),
            exam_number="NE0123456789",
        )
        for hour in range(6)
    ]
    # simulate possibly out of order eegs files
    shuffle(eegs)

    return eegs


@pytest.fixture
def patient(eegs: list[EEGFile]) -> Patient:
    patient = Patient(
        patient_id="notanid",
        patient_name="NOT A NAME, BOB",
        sex="Unknown",
        birth_date=datetime(1900, 1, 1),
        eegs=eegs,
    )

    # make sure eegs are sorted for tests later
    patient.eegs.sort()

    return patient


def test_nkpy_get_patient_eegs(patient: Patient) -> None:
    selected_eegs = nkpy.get_patient_eegs(
        patient=patient,
    )

    assert selected_eegs == patient.eegs


def test_nkpy_get_patient_eegs_before(patient: Patient) -> None:
    selected_eegs = nkpy.get_patient_eegs(
        patient=patient,
        before=datetime(2024, 1, 1, 3, 30),
    )

    assert selected_eegs == patient.eegs[:4]


def test_nkpy_get_patient_eegs_after(patient: Patient) -> None:
    selected_eegs = nkpy.get_patient_eegs(
        patient=patient,
        after=datetime(2024, 1, 1, 3, 30),
    )

    assert selected_eegs == patient.eegs[3:]


def test_nkpy_get_patient_eegs_before_after(patient: Patient) -> None:
    selected_eegs = nkpy.get_patient_eegs(
        patient=patient,
        before=datetime(2024, 1, 1, 4, 30),
        after=datetime(2024, 1, 1, 1, 30),
    )

    assert selected_eegs == patient.eegs[1:5]

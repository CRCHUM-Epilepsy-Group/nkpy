from __future__ import annotations

from datetime import datetime
from pathlib import Path
from random import shuffle

import pytest

import nkpy
from nkpy.excel import Patient, VideoFile


@pytest.fixture
def videos() -> list[VideoFile]:
    videos = [
        VideoFile(
            path=Path(),
            start=datetime(2024, 1, 1, hour, 0, 0),
            end=datetime(2024, 1, 1, hour, 59, 0),
            clipped=False,
        )
        for hour in range(6)
    ]
    # simulate possibly out of order video files
    shuffle(videos)

    return videos


@pytest.fixture
def patient(videos: list[VideoFile]) -> Patient:
    patient = Patient(
        patient_id="notanid",
        patient_name="NOT A NAME, BOB",
        sex="Unknown",
        birth_date=datetime(1900, 1, 1),
        videos=videos,
    )

    # make sure videos are sorted for tests later
    patient.videos.sort()

    return patient


def test_nkpy_get_patient_videos(patient: Patient) -> None:
    selected_videos = nkpy.get_patient_videos(
        patient=patient,
    )

    assert selected_videos == patient.videos


def test_nkpy_get_patient_videos_before(patient: Patient) -> None:
    selected_videos = nkpy.get_patient_videos(
        patient=patient,
        before=datetime(2024, 1, 1, 3, 30),
    )

    assert selected_videos == patient.videos[:4]


def test_nkpy_get_patient_videos_after(patient: Patient) -> None:
    selected_videos = nkpy.get_patient_videos(
        patient=patient,
        after=datetime(2024, 1, 1, 3, 30),
    )

    assert selected_videos == patient.videos[3:]


def test_nkpy_get_patient_videos_before_after(patient: Patient) -> None:
    selected_videos = nkpy.get_patient_videos(
        patient=patient,
        before=datetime(2024, 1, 1, 4, 30),
        after=datetime(2024, 1, 1, 1, 30),
    )

    assert selected_videos == patient.videos[1:5]

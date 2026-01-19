from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

import nkpy

from . import config

if TYPE_CHECKING:
    from nkpy.excel import PatientDict


@pytest.fixture
def neuroworkbench_excel() -> Path:
    return config.neuroworkbench_excel


@pytest.fixture
def neuroworkbench_all_excels() -> list[Path]:
    return list(config.neuroworkbench_files_directory.glob("*.xls"))


@pytest.fixture
def neuroworkbench_routine_excel() -> Path:
    return config.neuroworkbench_routine_excel


@pytest.fixture
def neuroworkbench_patient_dict(neuroworkbench_excel: Path) -> PatientDict:
    return nkpy.read_excel(neuroworkbench_excel)


@pytest.fixture
def neuroworkbench_all_patient_dicts(
    neuroworkbench_all_excels: list[Path],
) -> list[PatientDict]:
    return [nkpy.read_excel(filename) for filename in neuroworkbench_all_excels]


@pytest.mark.parametrize(
    ("bool_list", "expected_ranges"),
    [
        ([True, True, False, True, True], [range(2), range(3, 5)]),
        ([False, False, True, True, True], [range(2, 5)]),
        (
            [True, False, True, False, False, True],
            [range(1), range(2, 3), range(5, 6)],
        ),
        ([True, True, True, True, True, True], [range(6)]),
        ([False, False, False, False, False, False], []),
        ([True] * 50 + [False], [range(50)]),
    ],
)
def test_get_blocks(bool_list: list[bool], expected_ranges: list[range]) -> None:
    assert nkpy.excel.get_blocks(bool_list) == expected_ranges


@pytest.mark.parametrize(
    "excel_file", [[f] for f in config.neuroworkbench_files_directory.glob("*.xls")]
)
def test_read_excel(excel_file: Path) -> None:
    patients = nkpy.read_excel(excel_file)
    assert isinstance(patients, dict)


def test_read__excel(neuroworkbench_excel: Path) -> None:
    patients = nkpy.read_excel(neuroworkbench_excel)
    assert isinstance(patients, dict)

    for patient in patients.values():
        assert isinstance(patient.patient_id, str)
        assert isinstance(patient.patient_name, str)
        assert isinstance(patient.sex, str)
        assert isinstance(patient.birth_date, datetime)

        for eeg in patient.eegs:
            assert isinstance(eeg.path, Path)
            assert isinstance(eeg.start, datetime)
            assert isinstance(eeg.end, datetime)
            assert isinstance(eeg.exam_number, str)

        for video in patient.videos:
            assert isinstance(video.path, Path)
            assert isinstance(video.start, datetime)
            assert isinstance(video.end, datetime)
            assert isinstance(video.clipped, bool)


def test_read_routine_excel(neuroworkbench_routine_excel: Path) -> None:
    patients = nkpy.read_excel(neuroworkbench_routine_excel)
    assert isinstance(patients, dict)

    for patient in patients.values():
        assert isinstance(patient.patient_id, str)
        assert isinstance(patient.patient_name, str)
        assert isinstance(patient.sex, str)
        assert isinstance(patient.birth_date, datetime)

        for eeg in patient.eegs:
            assert isinstance(eeg.path, Path)
            assert isinstance(eeg.start, datetime)
            assert isinstance(eeg.end, datetime)
            assert isinstance(eeg.exam_number, str)

        for video in patient.videos:
            assert isinstance(video.path, Path)
            assert isinstance(video.start, datetime)
            assert isinstance(video.end, datetime)
            assert isinstance(video.clipped, bool)


def test_read_excels(neuroworkbench_all_excels: list[Path]) -> None:
    nkpy.read_excels(*neuroworkbench_all_excels)


def test_read_excel_video_paths_exist(
    neuroworkbench_patient_dict: PatientDict,
) -> None:
    for patient in neuroworkbench_patient_dict.values():
        for video in patient.videos:
            assert video.path.exists()


def test_read_excel_eeg_paths_exist(
    neuroworkbench_patient_dict: PatientDict,
) -> None:
    for patient in neuroworkbench_patient_dict.values():
        for eeg in patient.eegs:
            assert eeg.path.exists()


def test_merge_patient_dicts_all_ids(
    neuroworkbench_all_patient_dicts: list[PatientDict],
) -> None:
    all_patients = nkpy.excel.merge_patient_dicts(*neuroworkbench_all_patient_dicts)
    all_patient_ids = set(all_patients.keys())

    for patient_dict in neuroworkbench_all_patient_dicts:
        ids = set(patient_dict.keys())
        assert (ids & all_patient_ids) == ids


def test_merge_patient_dicts_all_videos(
    neuroworkbench_all_patient_dicts: list[PatientDict],
) -> None:
    all_patients = nkpy.excel.merge_patient_dicts(*neuroworkbench_all_patient_dicts)

    for patient_id in all_patients:
        n_videos: int = 0
        patient_videos = []
        for patient_dict in neuroworkbench_all_patient_dicts:
            try:
                n_videos += len(patient_dict[patient_id].videos)
                patient_videos.extend([v.path for v in patient_dict[patient_id].videos])
            except KeyError:
                # patient not in this dict
                pass
        assert n_videos == len(all_patients[patient_id].videos), patient_id


def test_merge_patient_dicts_all_eegs(
    neuroworkbench_all_patient_dicts: list[PatientDict],
) -> None:
    all_patients = nkpy.excel.merge_patient_dicts(*neuroworkbench_all_patient_dicts)

    for patient_id in all_patients:
        n_eegs: int = 0
        patient_eegs = []
        for patient_dict in neuroworkbench_all_patient_dicts:
            try:
                n_eegs += len(patient_dict[patient_id].eegs)
                patient_eegs.extend([e.path for e in patient_dict[patient_id].eegs])
            except KeyError:
                # patient not in this dict
                pass
        assert n_eegs == len(all_patients[patient_id].eegs), patient_id

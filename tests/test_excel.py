from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

import nkpy

from . import config

if TYPE_CHECKING:
    from pathlib import Path

    from nkpy.excel import PatientDict


@pytest.fixture
def neuroworkbench_excel() -> Path:
    return config.neuroworkbench_excel


@pytest.fixture
def neuroworkbench_all_excels() -> list[Path]:
    return list(config.neuroworkbench_files_directory.glob("*.xls"))


@pytest.fixture
def neuroworkbench_patient_dict(neuroworkbench_excel: Path) -> PatientDict:
    return nkpy.read_excel(neuroworkbench_excel)


@pytest.fixture
def neuroworkbench_all_patient_dicts(
    neuroworkbench_all_excels: list[Path],
) -> list[PatientDict]:
    return [nkpy.read_excel(filename) for filename in neuroworkbench_all_excels]


def test_nkpy_read_excel(neuroworkbench_excel: Path) -> None:
    _ = nkpy.read_excel(neuroworkbench_excel)


def test_nkpy_read_excels(neuroworkbench_all_excels: list[Path]) -> None:
    nkpy.read_excels(*neuroworkbench_all_excels)


def test_nkpy_read_excel_paths_exist(neuroworkbench_patient_dict: PatientDict) -> None:
    for _, patient in neuroworkbench_patient_dict.items():
        for video in patient.videos:
            assert video.path.exists()


def test_all_excel_files(neuroworkbench_all_excels: list[Path]) -> None:
    for excel_file in neuroworkbench_all_excels:
        nkpy.read_excel(excel_file)


def test_nkpy_merge_patient_dicts_all_ids(
    neuroworkbench_all_patient_dicts: list[PatientDict],
) -> None:
    all_patients = nkpy.excel.merge_patient_dicts(*neuroworkbench_all_patient_dicts)
    all_patient_ids = set(all_patients.keys())

    for patient_dict in neuroworkbench_all_patient_dicts:
        ids = set(patient_dict.keys())
        assert (ids & all_patient_ids) == ids


def test_nkpy_merge_patient_dicts_all_videos(
    neuroworkbench_all_patient_dicts: list[PatientDict],
) -> None:
    all_patients = nkpy.excel.merge_patient_dicts(*neuroworkbench_all_patient_dicts)

    for patient_id in all_patients.keys():
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

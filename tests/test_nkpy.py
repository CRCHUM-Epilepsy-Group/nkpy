from pathlib import Path

import pytest

import nkpy

from . import config


@pytest.fixture
def neuroworkbench_excel() -> Path:
    return config.neuroworkbench_excel


@pytest.fixture
def neuroworkbench_all_excels() -> list[Path]:
    return list(config.neuroworkbench_files_directory.glob("*.xls"))


def test_nkpy_read_excel(neuroworkbench_excel: Path) -> None:
    nkpy.read_excel(neuroworkbench_excel)


def test_nkpy_read_excel_paths_exist(neuroworkbench_excel: Path) -> None:
    patients = nkpy.read_excel(neuroworkbench_excel)
    for _, videos in patients.items():
        for video in videos:
            assert video.path.exists()


def test_all_excel_files(neuroworkbench_all_excels: list[Path]) -> None:
    for excel_file in neuroworkbench_all_excels:
        nkpy.read_excel(excel_file)


def test_nkpy_merge_patient_dicts(neuroworkbench_all_excels: list[Path]) -> None:
    patient_dicts = [
        nkpy.read_excel(filename) for filename in neuroworkbench_all_excels
    ]
    all_excels = nkpy.excel.merge_patient_dicts(*patient_dicts)
    all_patients = set(all_excels.keys())

    for patient_dict in patient_dicts:
        ids = set(patient_dict.keys())
        assert (ids & all_patients) == ids

    for patient_id, videos in all_excels.items():
        n_videos: int = 0
        for patient_dict in patient_dicts:
            n_videos += len(patient_dict[patient_id])

        assert n_videos == len(videos)


def test_nkpy_read_excels(neuroworkbench_all_excels: list[Path]) -> None:
    nkpy.read_excels(*neuroworkbench_all_excels)

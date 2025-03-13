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
    print()
    nkpy.read_excel(neuroworkbench_excel)


def test_all_excel_files(neuroworkbench_all_excels: list[Path]) -> None:
    for excel_file in neuroworkbench_all_excels:
        nkpy.read_excel(excel_file)

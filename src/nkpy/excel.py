from __future__ import annotations

import logging
from copy import copy
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import xlrd

if TYPE_CHECKING:
    from typing import TYPE_CHECKING, Any, TypeAlias, TypedDict

    from xlrd.book import Book
    from xlrd.sheet import Cell, Rowinfo, Sheet

    PatientDict: TypeAlias = dict[str, "Patient"]

    PatientInfoDict = TypedDict(
        "PatientInfoDict",
        {
            "ID": str,
            "Patient Name": str,
            "Sex": str,
            "Birth Date": datetime,
            "Start": datetime | None,
            "End": datetime | None,
        },
    )
    VideoInfoDict = TypedDict(
        "VideoInfoDict",
        {
            "Path": str,
            "Video Name": str,
            "Start": datetime,
            "End": datetime,
            "Clipped": bool,
        },
    )

__all__ = [
    "read_excel",
    "read_excels",
    "CorruptionError",
    "VideoFile",
]

LOG = logging.getLogger(__name__)


class CorruptionError(Exception): ...


@dataclass
class Patient:
    patient_id: str
    patient_name: str
    sex: str
    birth_date: datetime
    videos: list[VideoFile] = field(default_factory=list)
    eegs: ... = field(default_factory=list)


@dataclass
class VideoFile:
    path: Path
    start: datetime
    end: datetime
    clipped: bool


@dataclass
class RowinfoProxy:
    outline_level: int = -1


def get_blocks(bool_list: list[bool], target_range: range | None = None) -> list[range]:
    if target_range is None:
        target_range = range(len(bool_list))

    blocks: list[range] = []
    start = None
    for i, value in enumerate(bool_list):
        if i not in target_range:
            continue

        if value:
            if start is None:
                start = i
        else:
            if start is not None:
                blocks.append(range(start, i))
                start = None

    if start is not None:
        blocks.append(range(start, target_range.stop))

    return blocks


def get_outline_levels(sheet: Sheet) -> list[int]:
    # Scanning for blocks based on collapse levels
    outline_levels: list[int] = []
    for i in range(sheet.nrows):
        rowinfo: Rowinfo | RowinfoProxy
        try:
            rowinfo = sheet.rowinfo_map[i]
        except KeyError:
            rowinfo = RowinfoProxy()

        assert rowinfo.outline_level is not None
        outline_levels.append(rowinfo.outline_level)

    # first row is always a header, not part of patient block
    outline_levels[0] = -1

    return outline_levels


def read_excel(filename: str | Path) -> PatientDict:
    try:
        workbook: Book = xlrd.open_workbook(str(filename), formatting_info=True)
        LOG.debug(f"Opened workbook {filename}")

    except xlrd.compdoc.CompDocError as e:
        raise CorruptionError(
            "Excel file is corrupted. Try opening it and saving "
            "it again with Excel to fix."
        ) from e

    def parse_cells(cells: list[Cell]) -> list[Any]:
        cell_values: list[Any] = []

        for cell in cells:
            if cell.ctype is xlrd.XL_CELL_DATE:
                cell_values.append(
                    xlrd.xldate_as_datetime(cell.value, workbook.datemode)
                )
            elif cell.value == "TRUE":
                cell_values.append(True)
            elif cell.value == "FALSE":
                cell_values.append(False)
            else:
                cell_values.append(cell.value)
        return cell_values

    patient_sheet = workbook.sheet_by_index(0)  # only one sheet anyway
    # we have 3 levels of ehaders, keep them in a dict for future reference
    headers: dict[int, list[str | float | datetime]] = {}
    LOG.debug("Reading headers[0]")
    headers[0] = parse_cells(patient_sheet.row(0))

    outline_levels = get_outline_levels(patient_sheet)
    patient_blocks = get_blocks([level >= 0 for level in outline_levels])
    recording_blocks = [
        get_blocks([level >= 2 for level in outline_levels], patient_block)
        for patient_block in patient_blocks
    ]

    patients: PatientDict = {}
    for patient_range, recording_ranges in zip(patient_blocks, recording_blocks):
        patient_info: PatientInfoDict = dict(
            zip(headers[0], parse_cells(patient_sheet.row(patient_range.start)))
        )  # type: ignore

        if 1 not in headers:
            LOG.debug("Reading headers[1]")
            headers[1] = parse_cells(patient_sheet.row(patient_range.start + 2))

        patient = Patient(
            patient_id=patient_info["ID"],
            patient_name=patient_info["Patient Name"],
            sex=patient_info["Sex"],
            birth_date=patient_info["Birth Date"],
        )
        patients[patient.patient_id] = patient

        for recordings in recording_ranges:
            if 2 not in headers:
                LOG.debug("Reading headers[2]")
                headers[2] = parse_cells(patient_sheet.row(recordings.start + 1))

            for i, row in enumerate(recordings):
                if i < 2:
                    # skip the first 2 rows, which are headers
                    continue

                video_info: VideoInfoDict = dict(
                    zip(headers[2], parse_cells(patient_sheet.row(row)))
                )  # type: ignore

                patients[patient_info["ID"]].videos.append(
                    VideoFile(
                        path=Path(video_info["Path"]) / video_info["Video Name"],
                        start=video_info["Start"],
                        end=video_info["End"],
                        clipped=video_info["Clipped"],
                    )
                )
        LOG.debug(
            f"Found a total of {len(patients[patient_info['ID']].videos):>4d} videos "
            f"for patient {patient_info['ID']}"
        )

    return patients


def merge_patient_dicts(*patient_dicts: PatientDict) -> PatientDict:
    merged_patient_dict: PatientDict = {}
    for patient_dict in patient_dicts:
        for patient_id, patient in patient_dict.items():
            try:
                merged_patient_dict[patient_id].videos.extend(patient.videos)
            except KeyError:
                # create a new Patient to avoid multiple reference issues
                merged_patient_dict[patient_id] = Patient(
                    patient_id=patient.patient_id,
                    patient_name=patient.patient_name,
                    sex=patient.sex,
                    birth_date=patient.birth_date,
                    videos=copy(patient.videos),
                )

    return merged_patient_dict


def read_excels(*filenames: str | Path) -> PatientDict:
    return merge_patient_dicts(*(read_excel(filename) for filename in filenames))

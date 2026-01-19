from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime

    from .excel import Patient, VideoFile

__all__ = [
    "get_patient_videos",
]


def get_patient_videos(
    patient: Patient,
    before: datetime | None = None,
    after: datetime | None = None,
) -> list[VideoFile]:
    """Select the videos from a :class:`Patient` that are within a time range.

    Parameters
    ----------
    patient : :class:`Patient`
        The :class:`Patient` object from which we want to select the :class:`VideoFile`.
    before : :class:`datetime.datetime` | ``None``, optional
        The :class:`datetime.datetime` which we want the videos that are before that
        moment. If ``None``, select all videos up to the end of the recordings.
        By default ``None``.
    after : :class:`datetime.datetime` | ``None``, optional
        The :class:`datetime.datetime` which we want the videos that are after that
        moment. If No``None``ne, select all videos from the start of the recordings.
        By default ``None``.

    Returns
    -------
    list[:class:`VideoFile`]
        List of the selected :class:`VideoFile`.

    """
    selected_videos = patient.videos

    if before is not None:
        selected_videos = [video for video in selected_videos if video.start <= before]

    if after is not None:
        selected_videos = [video for video in selected_videos if after <= video.end]

    return selected_videos

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime

    from .excel import EEGFile, Patient

__all__ = [
    "get_patient_eegs",
]


def get_patient_eegs(
    patient: Patient,
    before: datetime | None = None,
    after: datetime | None = None,
) -> list[EEGFile]:
    """Select the eegs from a :class:`Patient` that are within a time range.

    Parameters
    ----------
    patient : Patient
        The :class:`Patient` object from which we want to select the :class:`EEGFile`.
    before : :class:`datetime.datetime` | ``None``, optional
        The :class:`datetime.datetime` which we want the eegs that are before that
        moment. If ``None``, select all eegs up to the end of the recordings.
        By default ``None``.
    after : :class:`datetime.datetime` | ``None``, optional
        The :class:`datetime.datetime` which we want the eegs that are after that
        moment. If ``None``, select all eegs from the start of the recordings.
        By default ``None``.

    Returns
    -------
    list[:class:`EEGFile`]
        List of the selected :class:`EEGFile`.

    """
    selected_eegs = patient.eegs

    if before is not None:
        selected_eegs = [eeg for eeg in selected_eegs if eeg.start <= before]

    if after is not None:
        selected_eegs = [eeg for eeg in selected_eegs if after <= eeg.end]

    return selected_eegs

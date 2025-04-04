Examples
========

Reading
-------

Reading an Excel file exported from Nihon Kohden's NeuroWorkbench:

.. code-block:: python

    from pathlib import Path
    import nkpy

    # Read one Excel file
    patient_dict = nkpy.read_excel("path/to/neuroworkbench.xls")

    # Read many Excel files at once
    excel_files = list(Path("path/to/excel/directory").glob("*.xls"))
    patient_dict = nkpy.read_excels(*excel_files)

    print(patient_dict)
    # {"S0123456": <Patient>, ...}

EEGs
------

Get the EEGs after April 1st, 2024 from a patient with ID :code:`S0123456`:

.. code-block:: python

    from datetime import datetime

    # Select the patient with corresponding ID
    patient_id = "S0123456"
    patient = patient_dict[patient_id]
    # Set the date as a datetime object
    after = datetime(2024, 4, 1)  # after April 1st, 2024

    # get the videos from the Patient object
    eegs = nkpy.get_patient_eegs(patient, after=after)

    print(eegs)
    # [<EEGFile 0>, <EEGFile 1>, ...]

Manipulate the EEG information with the :class:`nkpy.EEGFile` objects:

.. code-block:: python

    eeg = patient.eegs[0]

    # Get the full path of the file
    print(eeg.path)
    # Path(path/to/eeg_file.EEG)

    # Get the duration of the recording
    print(eeg.end - eeg.start)
    # datetime.timedelta(hours=1)

    # Get the exam number of the EEG
    print(video.exam_number)
    # NE0123456789

Videos
------

Get the videos after April 1st, 2024 from a patient with ID :code:`S0123456`:

.. code-block:: python

    from datetime import datetime

    # Select the patient with corresponding ID
    patient_id = "S0123456"
    patient = patient_dict[patient_id]
    # Set the date as a datetime object
    after = datetime(2024, 4, 1)  # after April 1st, 2024

    # get the videos from the Patient object
    videos = nkpy.get_patient_videos(patient, after=after)

    print(videos)
    # [<VideoFile 0>, <VideoFile 1>, ...]

Manipulate the video information with the :class:`nkpy.VideoFile` objects:

.. code-block:: python

    video = patient.videos[0]

    # Get the full path of the file
    print(video.path)
    # Path(path/to/video_file.m2t)

    # Get the duration of the recording
    print(video.end - video.start)
    # datetime.timedelta(hours=1)

    # Check if the video was clipped
    print(video.clipped)
    # False

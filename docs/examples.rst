Examples
========

Reading
-------

Reading an Excel file exported from Nihon Kohden's NeuroWorkbench:

.. code-block:: py

    from pathlib import Path
    import nkpy

    # Read one Excel file
    patient_dict = nkpy.read_excel("path/to/neuroworkbench.xls")

    # Read many Excel files at once
    excel_files = list(Path("path/to/excel/directory").glob("*.xls"))
    patient_dict = nkpy.read_excels(*excel_files)

    print(patient_dict)
    # {"S0123456": <Patient>, ...}

Videos
------

Get the videos after April 1st, 2024 from a patient with ID :code:`S0123456`:

.. code-block:: py

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

.. code-block:: py

    video = patient.video[0]

    # Get the full path of the file
    print(video.path)
    # Path(path/to/video_file.m2t)

    # Get the duration of the recording
    print(video.end - video.start)
    # datetime.timedelta(hours=1)

    # Check if the video was clipped
    print(video.clipped)
    # False

.. nkpy documentation master file, created by
   sphinx-quickstart on Wed Mar 19 10:48:49 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

nkpy documentation
==================

.. Add your content using ``reStructuredText`` syntax. See the
.. `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
.. documentation for details.

Library to read patient information from extracted Excel files from Nihon Kohden's NeuroWorkbench software.

Currently only extracts video information such as their path, start date and end date.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   excel
   nkpy
   examples

Installation
------------

To install the package in your project, you have two options:

With ``uv``
^^^^^^^^^^^
.. code-block:: bash

   # if the project does not already exist
   uv init my-project
   cd my-project

   uv add git+https://github.com/CRCHUM-Epilepsy-Group/nkpy.git

With ``pip``
^^^^^^^^^^^^
.. code-block:: bash

   pip install git+https://github.com/CRCHUM-Epilepsy-Group/nkpy.git


Logging
-------

Enable logging for the module with:

.. code-block:: python

   import logging

   logger = logging.get_Logger("nkpy")
   logger.setLevel(logging.DEBUG)
   logger.addHandler(logging.StreamHandler())


Links
-----
- `GitHub Repository <https://github.com/CRCHUM-Epilepsy-Group/nkpy>`_

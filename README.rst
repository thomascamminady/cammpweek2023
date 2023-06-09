=========================
Automatic Climb Detection
=========================






Install
--------
Before running ``make init``, make sure that all necessary components are installed.
For MacOS this would be

.. code-block:: bash

   brew install git git-lfs poetry visual-studio-code


To set up the project, simply run

.. code-block:: bash

   make init

Next, activate the ``poetry`` environment via

.. code-block:: bash

   poetry shell


Parse GPX files
-------
Parse all files in a folder

.. code-block:: bash

   poetry run python  automatic_climb_detection/gpx_to_csv.py --input data/TourDeFrance2022/


Parse only a single file

.. code-block:: bash

   poetry run python  automatic_climb_detection/gpx_to_csv.py --input data/TourDeFrance2022/stage-1-gpxroute.gpx

Data
-------
- Tour de France 2022 GPX files taken from Cyclingstage_.


Credits
-------

This package was created with Cookiecutter_ and `thomascamminady/cookiecutter-pypackage`_, a fork of the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`thomascamminady/cookiecutter-pypackage`: https://github.com/thomascamminady/cookiecutter-pypackage
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _Cyclingstage: https://www.cyclingstage.com/tour-de-france-2022-gpx/

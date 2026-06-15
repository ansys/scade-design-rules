Getting started
###############
To use Ansys SCADE Design Rules, you must have a valid license for Ansys SCADE.

For information on getting a licensed copy, see the
`Ansys SCADE Suite <https://www.ansys.com/products/embedded-software/ansys-scade-suite>`_
page on the Ansys website.

Requirements
============
The ``ansys-scade-design-rules`` package supports only the versions of Python delivered with
Ansys SCADE, starting from 2021 R2:

* 2021 R2 to 2023 R1: Python 3.7
* 2023 R2 and later: Python 3.10

Install in user mode
====================
The following steps are for installing Ansys SCADE Design Rules in user mode. If you want to
contribute to Ansys SCADE Design Rules, see :ref:`contribute_scade_design_rules`
for installing in developer mode.

#. Before installing Ansys SCADE Design Rules in user mode, run this command to ensure that
   you have the latest version of `pip`_:

   .. code:: bash

      python -m pip install -U pip

#. Install Ansys SCADE Design Rules with this command:

   .. code:: bash

       python -m pip install --user ansys-scade-design-rules

   The option ``--user`` makes the package accessible by all SCADE releases:

Install in user mode
####################
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

.. LINKS AND REFERENCES
.. _pip: https://pypi.org/project/pip/

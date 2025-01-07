Metrics
=======

The following guidelines ensure the consistency of the repository and allow some automated verifications and tasks.

* A metric shall be defined in a Python script, located in the ``metrics`` sub-directory.
* The name of the script is the pythonized name of the rule. For example, ``NumberOfOutgoingTransitionsPerState`` is defined in
  ``metrics/number_of_outgoing_transitions_per_state.py``.
* The class defining the rule shall inherit from ``ansys.scade.design_rules.utils.Metric`` (TODO link).
  This is first meant for debugging and testing purposes. This class adds a few services to facilitate the design
  or customization of a metric.
* The ``id`` attribute of the metric must be ``id_<number>`` where ``<number>`` is a four digit number,
  for example ``id_0007``. The ``ansys.scade.design_rules.catalog.txt`` file lists all the existing metrics and rules,
  sorted by ``id``: When creating a new metric, use the next available id, that is the last one plus 1.
  The catalog is automatically updated by pre-commit hooks.
* The file shall be usable directly by *SCADE Metrics and Rules Checker*, at least for the examples or unit tests.
  This implies to:

  * Add the location of ``ansys.scade.design_rules.utils.Metric`` to the Python path at the beginning of the file:

    .. code::

       if __name__ == '__main__':
          # metric instantiated outside of a package
          from os.path import abspath, dirname
          import sys

          sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))

  * Provide an instantiation with default parameters at the end of the file:

    .. code::

       if __name__ == '__main__':
          # metric instantiated outside of a package
          MyMetric()

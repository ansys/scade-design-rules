Rules
=====

The following guidelines ensure the consistency of the repository and allow some automated verifications and tasks.

* A rule shall be defined in a Python script, located in a sub-directory corresponding to a category.
* The name of the script is the pythonized name of the rule. For example, ``CamelCaseNaming`` is defined in
  ``naming/camel_case_naming.py``.
* The class defining the rule shall inherit from ``ansys.scade.design_rules.utils.Rule`` (TODO link).
  This is first meant for debugging and testing purposes. This class adds a few services to facilitate the design
  or customization of a rule.
* The file shall be usable directly by *SCADE Metrics and Rules Checker*, at least for the examples or unit tests.
  This implies to:

  * Add the location of ``ansys.scade.design_rules.utils.Rule`` to the Python path at the beginning of the file:

    .. code::

       if __name__ == '__main__':
          # rule instantiated outside of a package
          from os.path import abspath, dirname
          import sys

          sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))

  * Provide an instantiation with default parameters at the end of the file:

    .. code::

       if __name__ == '__main__':
          # rule instantiated outside of a package
          MyRule()

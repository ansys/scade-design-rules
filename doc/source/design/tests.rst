Tests
=====

The testing environment is based on ``pytest``. The ``./tests/utils/conftest.py``
file provides means to load a Scade model once during a test session.

Before creating tests for a new rule, it is advised to find the closest existing tests,
and use them as a template:

* How to design a test model
* How to instantiate a rule
* How to load a model
* How to parameterize tests

Hint: Some test models have Python scripts that output a template for
the parametrization of the tests. It is advised to reuse such design
as much as possible to ease the maintenance.

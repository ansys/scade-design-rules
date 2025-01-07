Repository
==========
The overall structure of the repository is as follows:

.. code::

  + <root>
     + doc/source/metrics
     |  index.rst
     |  <metric1>.rst
     |  <metric2>.rst
     |  ...
     |  + ...
     + doc/source/rules
     |  + <category1>
     |  |  index.rst
     |  |  <rule1>.rst
     |  |  <rule2>.rst
     |  |  ...
     |  + ...
     + examples
     |  + <category1>
     |  |  + <rule1>
     |  |  |  <rule1>.etp
     |  |  |  ...
     |  |  + <rule2>
     |  |  |  <rule2>.etp
     |  |  |  ...
     |  |  + ...
     |  + ...
     + src/ansys/scade/design_rules
     |  + metrics
     |  |  <metric1>.py
     |  |  <metric2>.py
     |  |  ...
     |  + <category1>
     |  |  <rule1>.py
     |  |  <rule2>.py
     |  |  ...
     |  + ...
     + tests
     |  + metrics
     |  |  test_<metric1>.py
     |  |  test_<metric2>.py
     |  |  ...
        + <category1>
        |  test_<rule1>.py
        |  test_<rule2>.py
        |  ...
        + ...

This schema represents only the directories and files relative to the metrics and rules.

A ``tools`` directory contains scripts used to ensure the repository's structure consistency,
or the documentation consistency.

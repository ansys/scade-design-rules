Repository
==========
The overall structure of the repository is as follows:

.. code::

  + <root>
     + doc/source/rules
     |  + <category1>
     |  |  content.rst
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
     |  + <category1>
     |  |  <rule1>.py
     |  |  <rule2>.py
     |  |  ...
     |  + ...
     + tests
        + <category1>
        |  test_<rule1>.py
        |  test_<rule2>.py
        |  ...
        + ...

This schema represents only the directories and files relative to the rules.

A ``tools`` directory contains scripts used to ensure the repository's structure consistency,
or the documentation consistency.

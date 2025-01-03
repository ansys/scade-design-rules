.. index:: single: Maximum diagrams per element

Maximum diagrams per element
============================

.. rule::
   :filename: maximum_diagrams_per_element.py
   :class: MaximumDiagramsPerElement
   :id: id_0065
   :reference: n/a
   :kind: generic
   :tags: structure

   Maximum diagrams per element

Description
-----------

.. start_description

Maximum diagrams defining an operator, a state, or an action.
Parameter: maximum value: e.g.: '7'

.. end_description

Rationale
---------
This enforces compliance with a specific modeling standard by placing an upper bound on the number of graphical diagrams for each model element.

Verification
------------
This rule checks all operators, state machines, state machine actions/states, and variables in the model.
It counts the number of graphical diagrams associated to each element.

The rule fails if the limit exceeds the authorized maximum.

Resolution
----------
Modify the offending element to reduce its number of diagrams, as detailed in the rule failure message.

Customization
-------------
TODO

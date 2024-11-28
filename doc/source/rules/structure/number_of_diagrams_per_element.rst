.. index:: single: Number of diagrams per element

Number of diagrams per element
==============================

.. rule::
   :filename: number_of_diagrams_per_element.py
   :class: NumberOfDiagramsPerElement
   :id: id_0065
   :reference: n/a
   :kind: generic
   :tags: structure

   Number of diagrams per element

Description
-----------

.. start_description

Number of diagrams defining an operator, a state, or an action.
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

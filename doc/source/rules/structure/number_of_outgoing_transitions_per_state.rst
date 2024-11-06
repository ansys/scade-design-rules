.. index:: single: Number Of Outgoing Transitions Per State

Number Of Outgoing Transitions Per State
========================================

.. rule::
   :filename: number_of_outgoing_transitions_per_state.py
   :class: NumberOfOutgoingTransitionsPerState
   :id: id_0072
   :reference: n/a
   :kind: generic
   :tags: structure

   Number of outgoing transitions per state

Description
-----------

.. start_description

Number of outgoing transitions per state.
Parameter: maximum value: e.g.: '7'

.. end_description

The rule parameter is an integer value describing the maximum authorized transitions per state. Default value is ``7``.

Rationale
---------
This enforces compliance with a specific modeling standard by placing an upper bound on outgoing transitions for any state machine state.

Verification
------------
This rule checks all state machine states in the model. For each one, it counts the number of outgoing transitions.
The rule fails if outgoing transitions exceed the authorized maximum.

Resolution
----------
Modify the offending state machine state to reduce its number of outgoing transitions.

Customization
-------------
N/A.

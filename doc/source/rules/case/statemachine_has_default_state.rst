.. index:: single: Statemachine Has Default State

Statemachine Has Default State
==============================

.. rule::
   :filename: statemachine_has_default_state.py
   :class: StatemachineHasDefaultState
   :id: id_0105
   :reference: n/a
   :kind: generic
   :tags: case

   State machine default checked

Description
-----------

.. start_description

In the SCADE model, each state machine shall use the 'default' for one state to catch any abnormal value.

.. end_description

Rationale
---------
This ensures a defensive design to catch any abnormal value of enumerated data produced by the environment or by an imported operator.

Verification
------------
This rule iterates over state machine definitions and checks that at least one element bears pragma text `default`.

Resolution
----------
Modify the offending state machine to add a ``default`` state.

Customization
-------------
N/A.

.. index:: single: Transition Actions

Transition Actions
==================

.. rule::
   :filename: transition_actions.py
   :class: TransitionActions
   :id: id_0084
   :reference: n/a
   :kind: generic
   :tags: modelling

   No transition actions except signal emissions.

Description
-----------

.. start_description

There shall be no action in transitions except signal emission.

.. end_description

Rationale
---------
This enforces compliance with a specific modeling standard by ensuring that state machine transition actions are either empty or limited to emitting signals.

Verification
------------
This rule checks whether any state machine transition in the model contains an action other than emitting a signal, and fails if it finds one.

Resolution
----------
Modify the offending transition, as detailed in the rule failure message.

Customization
-------------
N/A.

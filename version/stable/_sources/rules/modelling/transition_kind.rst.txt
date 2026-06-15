.. index:: single: Transition kind

Transition kind
###############

.. rule::
   :filename: transition_kind.py
   :class: TransitionKind
   :id: id_0085
   :reference: n/a
   :kind: generic
   :tags: modelling

   Transition Kind

Description
===========

.. start_description

This rule checks that all transitions of a state machine are of the same kind, are all strong or are all weak transitions.
parameter: strong, weak, nomix: e.g.: 'nomix'

.. end_description

Rationale
=========
This enforces compliance with a specific modeling standard by ensuring that state machines only include one type of transition.

Verification
============
This rule checks each state machine throughout the model. For each state machine, it tallies weak/synchro transitions and strong transitions.

Depending on parameter value, it then verifies that only strong transitions are used, only weak/synchro transitions are used,
or that each state machine only uses one type of transition.

Resolution
==========
Modify the offending state machine, as detailed in the rule failure message.

Customization
=============
N/A.

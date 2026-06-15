.. index:: single: Maximum outgoing transitions per state

Maximum outgoing transitions per state
######################################

.. rule::
   :filename: maximum_outgoing_transitions_per_state.py
   :class: MaximumOutgoingTransitionsPerState
   :id: id_0072
   :reference: SDR-30-6
   :kind: generic
   :tags: structure

   Maximum outgoing transitions per state

Description
===========

.. start_description

Maximum outgoing transitions per state.
Parameter: maximum value: e.g.: '7'

.. end_description

The rule parameter is an integer value describing the maximum authorized transitions per state. Default value is ``7``.

Rationale
=========
This enforces compliance with a specific modeling standard by placing an upper bound on outgoing transitions for any state machine state.

Verification
============
This rule checks all states in the model. For each one, it retrieves the :ref:`Number of outgoing transitions per state <MetricNumberOfOutgoingTransitionsPerState>` metric.
The rule fails if outgoing transitions exceed the authorized maximum.

Resolution
==========
Modify the offending state to reduce its number of outgoing transitions.

Customization
=============
This rule depends on the :ref:`Number of outgoing transitions per state <MetricNumberOfOutgoingTransitionsPerState>`
metric, that must be included in the package. If you customize the ID of this metric, you must
provide it when instantiating the rule, using the parameter ``metric_id``.

Cf. :ref:`ug_customization` for an example.

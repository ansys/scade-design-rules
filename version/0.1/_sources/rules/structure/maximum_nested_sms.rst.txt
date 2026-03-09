.. index:: single: Maximum nested state machines

Maximum nested state machines
#############################

.. rule::
   :filename: maximum_nested_sms.py
   :class: MaximumNestedSMs
   :id: id_0070
   :reference: SDR-30-4
   :kind: generic
   :tags: structure

   Maximum nested SMs

Description
===========

.. start_description

Maximum hierarchical levels of nested state machines.
Parameter: maximum value: e.g.: '5'

.. end_description

The rule parameter is an integer value describing the maximum authorized depth for nested state machines. Default value is ``5``.

Rationale
=========
This enforces compliance with a specific modeling standard by placing an upper bound on the number of nested state machines.

Verification
============
This rule checks all state machines throughout the model.
It retrieves the :ref:`Number of nested state machines <MetricNumberOfNestedSMs>` metric associated to each state machine.

The rule fails if the maximum number of nested state machines exceeds the authorized value.

Resolution
==========
Consider refactoring the offending state machine to reduce the number of nested state machines.

Customization
=============
This rule depends on the :ref:`Number of nested state machines <MetricNumberOfNestedSMs>`
metric, that must be included in the package. If you customize the ID of this metric, you must
provide it when instantiating the rule, using the parameter ``metric_id``.

Cf. :ref:`ug_customization` for an example.

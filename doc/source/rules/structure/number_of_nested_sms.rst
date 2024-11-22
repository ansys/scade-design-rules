.. index:: single: Number Of Nested State Machines

Number of nested state machines
===============================

.. rule::
   :filename: number_of_nested_sms.py
   :class: NumberOfNestedSMs
   :id: id_0070
   :reference: n/a
   :kind: generic
   :tags: structure

   Number of nested SMs

Description
-----------

.. start_description

Number of hierarchical levels of nested state machines.
Parameter: maximum value: e.g.: '5'

.. end_description

The rule parameter is an integer value describing the maximum authorized depth for nested state machines. Default value is ``5``.

Rationale
---------
This enforces compliance with a specific modeling standard by placing an upper bound on the number of nested state machines.

Verification
------------
This rule checks all state machines throughout the model. For each one,
it uses a recursive depth-first algorithm to count the maximum number of nested state machines.

The rule traverses nested conditional blocks to look for enclosed state machines.
A state machine with no child state machine has a depth of ``1``.

The rule fails if the maximum number of nested state machines exceeds the authorized value.

Resolution
----------
Consider refactoring the offending state machine to reduce the number of nested state machines.

Customization
-------------
N/A.

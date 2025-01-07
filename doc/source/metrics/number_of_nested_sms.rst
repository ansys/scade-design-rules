.. index:: single: Number of nested state machines

Number of nested state machines
===============================

.. metric::
   :filename: number_of_nested_sms.py
   :class: NumberOfNestedSMs
   :id: id_0129
   :reference: n/a
   :kind: specific
   :tags: metrics

   Number of nested state machines

Description
-----------

.. start_description

Number of nested state machines.

.. end_description

Computation
-----------
The metric uses a recursive depth-first algorithm to count the maximum number of nested state machines.
The rule traverses nested conditional blocks to look for enclosed state machines.

A state machine with no child state machine has a depth of ``1``.

Customization
-------------
N/A.

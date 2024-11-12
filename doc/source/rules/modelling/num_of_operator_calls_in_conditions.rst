.. index:: single: Number Of Operator Calls In Conditions

Number Of Operator Calls In Conditions
======================================

.. rule::
   :filename: num_of_operator_calls_in_conditions.py
   :class: NumOfOperatorCallsInConditions
   :id: id_0075
   :reference: n/a
   :kind: generic
   :tags: modelling

   Number of operator calls in conditions

Description
-----------

.. start_description

Number of logical/comparison operator calls within conditions at Transitions or IfNodes.
Number and Exceptions given as parameters: 'calls=number,exc=op1;op2;etc.'

.. end_description

Default parameter value is ``4`` maximum calls, with array access excluded from call limit calculations.

Rationale
---------
This enforces compliance with a specific modeling standard by defining a maximum number of possible comparisons inside If Nodes and state machine transitions.

Verification
------------
This rule checks all If Node conditions inside of If Blocks, and every transition condition inside state machines.

For each one, it recursively counts the uses of comparison predefined operators:
array access, ``AND``, ``OR``, ``XOR``, ``NOT``, ``#``, ``<``, ``<=``, ``>``, ``>=``, ``=``, ``<>``.
Any of the operators may be excluded from the count by using the parameter.

The rule fails if any condition has a count greater than the call limit.

Resolution
----------
Modify the offending condition to reduce the number of comparison operator calls.

Customization
-------------
N/A.

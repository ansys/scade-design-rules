.. index:: single: Constant If Then Else

Constant If Then Else
=====================

.. rule::
   :filename: constant_if_then_else.py
   :class: ConstantIfThenElse
   :id: id_0011
   :reference: n/a
   :kind: generic
   :tags: if_then_else

   This operator should not be used with constant inputs of boolean type

Description
-----------

.. start_description

This rule checks if predefined Operators 'if..then..else' have constant boolean inputs on the left inputs

.. end_description

Rationale
---------
This enforces compliance with a specific modeling standard by ensuring that ``if..then..else`` operators do not use constant boolean inputs.
The intent is to promote direct use of a boolean expression instead of feeding it into an ``if..then..else`` and returning another, constant boolean.

Verification
------------
This rule checks all ``if..then..else`` calls throughout the model and verifies recursively whether either of their inputs is a raw boolean value.

Resolution
----------
Redesign the model to possibly remove the redundant ``if..then..else`` call.

Customization
-------------
N/A.

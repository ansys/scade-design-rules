.. index:: single: No Literals

No literals
===========

.. rule::
   :filename: no_literals.py
   :class: NoLiterals
   :id: id_0058
   :reference: n/a
   :kind: generic
   :tags: modelling

   No literals

Description
-----------

.. start_description

Literals shall only be used in constant values.
parameter: list of exceptions separated by comma: e.g.: 'true,false'

.. end_description

The rule parameter is as a comma-separated string that contains constant values that remain authorized. Default value is ``true, false``.

Rationale
---------
This enforces compliance with a specific modeling standard by ensuring that raw, literal values are not used directly in the model.

The intent is to improve readability by forbidding the use of "magic numbers" and relying on named constants instead.

Verification
------------
This rule checks expressions throughout the model and fails if it finds a raw literal value. The only places where a literal is allowed are:

* Constants
* Internal variable types
* Iterator accumulator values
* Case operator patterns
* Projection labels

Resolution
----------
Consider refactoring the offending literal into a constant.

Customization
-------------
N/A.

.. index:: single: Illegal Operations On Constants

Illegal operations on constants
===============================

.. rule::
   :filename: illegal_operations_on_constants.py
   :class: IllegalOperationsOnConstants
   :id: id_0028
   :reference: n/a
   :kind: generic
   :tags: modelling

   Illegal operations on constants

Description
-----------

.. start_description

Operator calls with only constant inputs shall not be used for the operators in parameter.
This rule does not apply for Constants and not for Types

.. end_description

The rule parameter is a comma-separated string containing predefined operators to check for calls with only constant inputs.
Available identifiers are documented in the SCADE Python API guide, under section *Access to Predefined Operators in Python*.
Default parameter value lists all predefined operators, except the ones that are dynamic in nature (such as the ``pre`` operator).

Rationale
---------
This enforces compliance with a specific modeling standard by ensuring that no computation flows in the model are fed with only constants.

One use case could be to enforce the creation of an exhaustive list of constants, instead of calculating some constants from others.

Verification
------------
This rule recursively checks that no operator in the model is fed with only constant values.

Resolution
----------
Replace the offending operator call with a dedicated constant, as detailed in the rule failure message.

Customization
-------------
N/A.

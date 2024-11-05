.. index:: single: Modulo Denominator Non Zero Constant

Modulo Denominator Non Zero Constant
====================================

.. rule::
   :filename: modulo_denominator_non_zero_constant.py
   :class: ModuloDenominatorNonZeroConstant
   :id: id_0119
   :reference: n/a
   :kind: specific
   :tags: modelling

   Modulo operations shall use a non zero constant as denominator.

Description
-----------

.. start_description

Modulo operations shall use a non zero constant as denominator.

.. end_description

Rationale
---------
This enforces compliance with a specific modeling standard by ensuring that modulo operations are only used with non-zero, constant denominators.

The intent is to enforce the use of one specific strategy to prevent runtime division-by-zero errors with modulos.
This strategy has the advantage of being statically verifiable (no need to execute the model).
In exchange, it forbids the use of modulo operations with dynamically-computed denominators.

Verification
------------
This rule checks all usages of predefined operator Modulo throughout the model.
For each, it attempts to determine the expression defining the denominator.
The rule fails if the expression does not statically resolve to a constant, or if it resolves to a constant that has value ``0``.

Resolution
----------
Modify the offending modulo call to use a denominator that resolves to a non-zero constant expression.

Customization
-------------
N/A.

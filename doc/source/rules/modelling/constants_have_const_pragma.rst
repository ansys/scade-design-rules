.. index:: single: Constants Have Const Pragma

Constants have const pragma
===========================

.. rule::
   :filename: constants_have_const_pragma.py
   :class: ConstantsHaveConstPragma
   :id: id_0106
   :reference: n/a
   :kind: generic
   :tags: modelling

   Constants Have Const Pragma

Description
-----------

.. start_description

Constants have the const pragma set.

.. end_description

Rationale
---------
This enforces compliance with a specific modeling standard by ensuring that constants make use of the ``const`` pragma.
This means that, in the generated C code, constants are declared as ``const`` instead of ``#define`` macros.

One possible use case is to ensure style homogeneity of the KCG-generated C code with external code with which it is meant to be integrated.

Verification
------------
This rule checks that all scalar constants have the ``C:const`` pragma defined.

Resolution
----------
Add the "Const" KCG pragma onto the offending constant.

Customization
-------------
N/A.

.. index:: single: Number Of Operators Per Package

Number of operators per package
===============================

.. rule::
   :filename: number_of_operators_per_package.py
   :class: NumberOfOperatorsPerPackage
   :id: id_0071
   :reference: n/a
   :kind: generic
   :tags: structure

   Number of operators per package

Description
-----------

.. start_description

Number of operators per package.

.. end_description

The rule parameter is an integer value describing the maximum authorized number of operators per package. Default value is ``10``.

Rationale
---------
This enforces compliance with a specific modeling standard by placing an upper bound on the number of operators in each package.

Verification
------------
This rule checks each package in the model. For each one, it counts the number of operators
and fails if the count exceeds the authorized maximum.

Resolution
----------
Modify the offending package to reduce its number of operators.

Customization
-------------
N/A.

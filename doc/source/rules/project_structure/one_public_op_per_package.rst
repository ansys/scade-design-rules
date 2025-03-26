.. index:: single: One public operator per package

One public operator per package
###############################

.. rule::
   :filename: one_public_op_per_package.py
   :class: OnePublicOpPerPackage
   :id: id_0076
   :reference: n/a
   :kind: generic
   :tags: project_structure

   Packages contain only one public operator.

Description
===========

.. start_description

This rule checks that each package only contains one public operator. All other operators shall be private.
parameter: maximum number: e.g.: '1'

.. end_description

Rationale
=========
This enforces compliance with a specific modeling standard by placing an upper bound on the number of public operators in each package.

Verification
============
This rule counts public operators in each of the model's packages. It fails if one package exceeds the number of allowed public operators.

Resolution
==========
Modify the offending package to contain at most the number of authorized public operators.

Customization
=============
N/A.

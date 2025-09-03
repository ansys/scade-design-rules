.. index:: single: Types taken from specific package

Types taken from specific package
#################################

.. rule::
   :filename: types_taken_from_specific_package.py
   :class: TypesTakenFromSpecificPackage
   :id: id_0101
   :reference: n/a
   :kind: specific
   :tags: project_structure

   Types from specific package

Description
===========

.. start_description

Interface data types from public operators are taken from specific packages.
parameter: list of packages separated by comma: e.g.: 'CHM, etc.'

.. end_description

Rationale
=========
This enforces compliance with a specific modeling standard by ensuring that only types defined in a given list of packages are used by public operators.

This rule is the opposite of rule :ref:`Types Not Taken From Specific Package <RuleTypesNotTakenFromSpecificPackage>`.

Verification
============
This rule checks all public operator inputs/outputs throughout the model. For each one,
it checks in which package its type is defined, and fails if that package is not in the authorized list.

Resolution
==========
Either modify the offending input/output type or make the operator private.

Customization
=============
TODO

.. seealso::
  * Rule :ref:`Types Not Taken From Specific Package <RuleTypesNotTakenFromSpecificPackage>`
  * Rule :ref:`Types Taken From Specific Project <RuleTypesTakenFromSpecificProject>`

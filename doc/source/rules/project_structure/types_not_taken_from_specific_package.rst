.. index:: single: Types not taken from specific package

Types not taken from specific package
=====================================

.. rule::
   :filename: types_not_taken_from_specific_package.py
   :class: TypesNotTakenFromSpecificPackage
   :id: id_0086
   :reference: n/a
   :kind: specific
   :tags: project_structure

   Types not from specific packages

Description
-----------

.. start_description

Interface data types from public operators shall not be taken from given packages.
parameter: list of packages separated by comma: e.g.: 'Obsolete,TobeAligned'

.. end_description

Rationale
---------
This enforces compliance with a specific modeling standard by ensuring that types defined in a given list of packages are not used by public operators.

This rule is the opposite of rule :ref:`Types Taken From Specific Package <RuleTypesTakenFromSpecificPackage>`.

Verification
------------
This rule checks all public operator inputs/outputs throughout the model.
For each one, it checks in which package its type is defined, and fails if that package is in the forbidden list.

Resolution
----------
Either modify the offending input/output type or make the operator private.

Customization
-------------
N/A.

.. seealso::
  * Rule :ref:`Types Taken From Specific Package <RuleTypesTakenFromSpecificPackage>`
  * Rule :ref:`Types Taken From Specific Project <RuleTypesTakenFromSpecificProject>`

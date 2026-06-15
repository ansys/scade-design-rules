.. index:: single: Types taken from specific project

Types taken from specific project
#################################

.. rule::
   :filename: types_taken_from_specific_project.py
   :class: TypesTakenFromSpecificProject
   :id: id_0087
   :reference: n/a
   :kind: specific
   :tags: project_structure

   Types from specific model/project

Description
===========

.. start_description

Interface data types from public operators are taken from Data Type Library project/model.
parameter: list of models separated by comma: e.g.: 'DataTypesLibs_Suite, etc.'

.. end_description

Rationale
=========
This enforces compliance with a specific modeling standard by ensuring that only types defined in a given list of projects are used by public operators.

This rule is similar to rule :ref:`Types Taken From Specific Package <RuleTypesTakenFromSpecificPackage>`.

Verification
============
This rule checks all public operator inputs/outputs throughout the model. For each one,
it checks in which model its type is defined, and fails if that model is not in the authorized list.

Resolution
==========
Either modify the offending input/output type or make the operator private.

Customization
=============
N/A.

.. seealso::
  * Rule :ref:`Types Taken From Specific Package <RuleTypesTakenFromSpecificPackage>`
  * Rule :ref:`Types Not Taken From Specific Package <RuleTypesNotTakenFromSpecificPackage>`

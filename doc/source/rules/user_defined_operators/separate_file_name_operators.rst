.. index:: single: Separate filename operators

Separate filename operators
===========================

.. rule::
   :filename: separate_file_name_operators.py
   :class: SeparateFileNameOperators
   :id: id_0082
   :reference: n/a
   :kind: generic
   :tags: user_defined_operators

   All operators should have the option Separate File Name checked or unchecked

Description
-----------

.. start_description

This rule checks that all operators have the option Separate File Name checked (``type=checked``) or unchecked ``type=dechecked``).

.. end_description

Rationale
---------
This ensures that multi-file management properties are homogeneous across a model. When Separate File Name is checked, each operator is saved into its own individual file, facilitating teamwork across a model.

Verification
------------
This rule verifies each operator in the model and ensures its Separate File Name property is in line with expectations.

Resolution
----------
Fix the Separate File Name property for offending operators.

Customization
-------------
N/A.

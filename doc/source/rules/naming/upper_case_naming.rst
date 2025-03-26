.. index:: single: Upper case name

Upper case name
###############

.. rule::
   :filename: upper_case_naming.py
   :class: UpperCaseNaming
   :id: id_0088
   :reference: SDR-21
   :kind: generic
   :tags: naming

   Uppercase letters

Description
===========
The words composing a name shall use uppercase letters, separated by a single '_' (underscore).

.. end_description

This rules applies to the following elements:

* Constant
* Enumeration value
* Operator parameter
* Polymorphic type

Rationale
=========
This enhances the readability of a model through homogeneous naming.

Verification
============
The rule registers to the specified elements of a Scade model and raises a violation when the name does not comply to the pattern.

Message: ``<name>: The name shall be composed of a sequence of uppercase words``

Resolution
==========
Rename the model element.

Customization
=============
The default value of the rule's parameters ``types`` or ``kinds`` can be overridden provided the targeted model elements have all a name.

Refer to the documentation of the instantiation of a rule for details.

.. seealso::
   * Instantiation of a rule

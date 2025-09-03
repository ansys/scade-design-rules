.. index:: single: Package name

Package name
###############

.. rule::
   :filename: name_structure_package.py
   :class: NameStructurePackage
   :id: id_0052
   :reference: SDR-22
   :tags: naming

   Package name

Description
===========
Package names shall be short (at most 10 characters for example).

.. end_description

If the length limit is not specified, they shall be acronyms, for example uppercase letters/digits only, no ``'_'`` (underscore).
Otherwise, they shall comply to the Pascal case naming convention.

The parameter defines the length limit with the following syntax: ``<length limit>`` (default value: ``10``).

Rationale
=========
This avoids too long names, either in the model or in the generated code.

Verification
============
The rule registers to the packages and raises a violation when:

* The length limit is not specified and the name is not an acronym

  Message: ``<name>: The name shall be an acronym``

* The length limit is specified and the name exceeds it

  Message: ``<name>: The name is longer than <length limit>``

* The length limit is specified and the name does not comply to the rule :ref:`Pascal case name <RulePascalCaseNaming>`

  Message: ``<name>: The name shall be composed of a sequence of words``

Resolution
==========
Rename the model element.

Customization
=============
N/A.

.. seealso::
  * Rule :ref:`Pascal case name <RulePascalCaseNaming>`

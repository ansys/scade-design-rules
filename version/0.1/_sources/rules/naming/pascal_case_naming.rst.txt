.. index:: single: Pascal case name

Pascal case name
################

.. rule::
   :filename: pascal_case_naming.py
   :class: PascalCaseNaming
   :id: id_0078
   :reference: SDR-11, SDR-12, SDR-13
   :kind: generic
   :tags: naming

   Pascal case name

Description
===========
Each word composing a name shall start with an uppercase letter;
The remainder of the word shall consist of lowercase letters and digits.

.. end_description

Exceptions:

* It is allowed to keep uppercase letters for acronyms of two words. Acronym of three letters or more shall use the pascal case convention, for example:

  .. vale off

  * systemIO --> system, IO
  * PIController --> PI, Controller
  * PidController --> Pid, Controller
  * PID1 --> PI, D1

  .. vale on

This rules applies to the following elements:

* User type
* Operator
* Diagram
* State machine
* State
* Activate if block
* Activate when block

Rationale
=========
This enhances the readability of a model through homogeneous naming.

This rule is commonly used with the rule :ref:`Camel case name <RuleCamelCaseNaming>`
which applies for variables of fields. It allows using the same base name for variables and types, for example ::

  function Xxx(speed : Speed)

Verification
============
The rule registers to the specified elements of a Scade model and raises a violation when the name does not comply to the pattern.

There are two dedicated messages for common mistakes:

* ``<name>: The name shall not contain '_'``
* ``<name>: The name shall start with a capital letter``
* ``<name>: The name shall be composed of a sequence of words``

Resolution
==========
Rename the model element.

Customization
=============
The default value of the rule's parameters ``types`` or ``kinds`` can be overridden provided the targeted model elements have all a name.

Refer to the documentation of the instantiation of a rule for details.

.. seealso::
  * Rule :ref:`Camel case name <RuleCamelCaseNaming>`
  * `Instantiation of a rule`

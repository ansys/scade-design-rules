.. index:: single: Camel case name

Camel case name
###############

.. rule::
   :filename: camel_case_naming.py
   :class: CamelCaseNaming
   :id: id_0008
   :reference: SDR-11, SDR-12, SDR-13
   :kind: generic
   :tags: naming

   Camel case name

Description
===========
Each word composing a name shall start with an uppercase letter except the first one.
The remainder of the word shall consist of lowercase letters and digits.

.. end_description

Exceptions:

* Scade keywords shall be suffixed by a trailing underscore ``_``, for example: ``state_``, ``sensor_``, etc.
* It is allowed to keep uppercase letters for acronyms of two words. Acronym of three letters or more shall use the pascal case convention, for example:

  .. vale off

  * systemIO --> System, IO
  * piController --> PI, Controller
  * enginePid --> Engine, PID
  * enginePID1 --> Engine, PI, D1

  .. vale on

This rules applies to the following elements:

* Field of a structure
* Sensor
* Input
* Hidden input
* Output
* Local variable
* Signal

Rationale
=========
This enhances the readability of a model through homogeneous naming.

This rule is commonly used with the rule :ref:`Pascal case name <RulePascalCaseNaming>`
which applies for declarations such as operators or types.
It allows using the same base name for variables and types, for example ::

  function Xxx(speed : Speed)

Verification
============
The rule registers to the specified elements of a Scade model and raises a violation when the name does not comply to the pattern.

There are two dedicated messages for common mistakes:

* ``<name>: The name shall not contain '_'``
* ``<name>: The name shall start with a lowercase letter``
* ``<name>: The name shall be composed of a sequence of words``

Resolution
==========
Rename the model element.

Customization
=============
The default value of the rule's parameters ``types`` or ``kinds`` can be overridden provided the targeted model elements have all a name.

Refer to the documentation of the instantiation of a rule for details.

.. seealso::
  * Rule :ref:`Pascal case name <RulePascalCaseNaming>`
  * Instantiation of a rule

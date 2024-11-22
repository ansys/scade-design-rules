.. index:: single: No Anonymous Type

No anonymous type
=================

.. rule::
   :filename: no_anonymous_type.py
   :class: NoAnonymousType
   :id: id_0122
   :reference: SDR-64
   :kind: specific
   :tags: modelling

   No anonymous type in the interface

Description
-----------

.. start_description

Only named types shall be used in root operator / imported operator interfaces. Anonymous types (example int^3) shall be avoided.
The rule applies to all the root operators, or the root operators of the specified configuration.

.. end_description

The parameter allows defining the name of a configuration, with the following syntax: ``configuration=<name>`` (default value: ``configuration=``).

Rationale
---------
Ensure user controlled naming of type declarations of root operators / imported operators.

Verification
------------
The rule registers to the inputs and outputs of a Scade model, and raises a violation for each
variable declared with an anonymous type, when the owning operator is root or is imported.

Message: ``The type <type definition> shall not be anonymous``.

* An operator is root if it doesn't have any instance in the model.
* The ``configuration`` parameter, when set, restricts the root operators to those specified for code generation.

Resolution
----------
Create a type with the same definition and use it in the variable's declaration.

Customization
-------------
N/A.

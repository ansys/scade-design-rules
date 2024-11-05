.. index:: single: Pragma Manifest

Pragma Manifest
===============

.. rule::
   :filename: pragma_manifest.py
   :class: PragmaManifest
   :id: id_0123
   :reference: SDR-65
   :kind: specific
   :tags: modelling

   Pragma manifest for complex types

Description
-----------
.. start_description

A pragma 'manifest' shall be used for each type declaration.
Optionally, the rule applies only for each type declaration used in the interface of a root operator / imported operator: Either all the root operators, or the ones of the specified configuration.

.. end_description

The parameter allows defining the name of a configuration and the applicable domain with the following syntax:
``configuration=<name>,interface=true|false`` (default value: ``configuration=,interface=false``).

Rationale
---------
Rationale: Ensure generated code stability and
user controlled naming of type declarations of root operators / imported operators.

Verification
------------
The rule registers to the types of a Scade model, and raises a violation for each
type whose equivalence class does not have a type with the KCG pragma ``manifest``.

Message: The type ``<type definition>`` has no KCG pragma "manifest".

* The rule applies only to arrays and structures.

When the parameter ``interface`` is set, the verification is restricted to the
types used in the declaration of a root operator or imported operator.

Message: The type ``<type definition>`` has no KCG pragma "manifest" and is used in the interface of root operators: <operators>``.

* An operator is root if it doesn't have any instance in the model.
* The ``configuration`` parameter, when set, restricts the root operators to those specified for code generation.

Resolution
----------
Set the KCG pragma ``manifest`` to the type.

Customization
-------------
N/A.

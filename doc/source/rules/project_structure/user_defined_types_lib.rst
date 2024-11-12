.. index:: single: User Defined Types Lib

User Defined Types Lib
======================

.. rule::
   :filename: user_defined_types_lib.py
   :class: UserDefinedTypesLib
   :id: id_0090
   :reference: n/a
   :kind: specific
   :tags: project_structure

   Check that user-defined complex types used in operators at top-level are located in libraries

Description
-----------

.. start_description

This rule checks if user-defined complex types used in top-level operators as interface are located in library projects prefixed with 'Lib' and the Domain name.

.. end_description

The rule parameter is a string describing the expected domain name prefix. Default value is ``Domain``.

Rationale
---------
This enforces compliance with a specific modeling standard by ensuring that all top-level operators use types defined in library packages that follow a given naming convention.

Verification
------------
This rule checks all inputs and outputs for top-level operators, that are operators located directly in a root-level package.

For each input/output that has a user-defined complex type, the rule checks that the type is defined in a separate library project.

Finally, it checks that the library project's name starts with 'Lib' + the domain name provided as a parameter, for example ``LibDomainProjectName``.

Resolution
----------
Modify the offending input/output type or move the type definition to an authorized library project.

Customization
-------------
N/A.

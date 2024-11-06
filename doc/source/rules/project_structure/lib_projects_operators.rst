.. index:: single: Lib Projects Operators

Lib Projects Operators
======================

.. rule::
   :filename: lib_projects_operators.py
   :class: LibProjectsOperators
   :id: id_0032
   :reference: n/a
   :kind: specific
   :tags: project_structure

   Library Projects shall not contain top-level Operators

Description
-----------

.. start_description

This rule checks if library Projects (prefixed with Lib) does not contain top-level Operators

.. end_description

The rule parameter describes the expected prefix for library projects. Default value is ``Lib``.

Rationale
---------
This enforces compliance with a specific modeling standard by ensuring that library projects do not define a top-level operator.

The intent is to ensure that library projects are always used by a main project instead of being run on their own.

Verification
------------
This rule checks whether the model name starts with the expected library prefix.
If so, it checks whether any operator is defined at the root of the model or in a top-level package, and fails if it finds one.

Resolution
----------
Move the offending operators to a lower-level package.

Customization
-------------
N/A.
